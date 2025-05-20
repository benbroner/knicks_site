import os
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.basketball-reference.com"
SCHEDULE_URL = f"{BASE_URL}/teams/NYK/2024_games.html"  # update year as needed
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BOX_DIR = os.path.join(DATA_DIR, 'box_scores')

os.makedirs(BOX_DIR, exist_ok=True)


def fetch_schedule():
    resp = requests.get(SCHEDULE_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find('table', id='games')
    if table is None:
        # table is often wrapped in HTML comments
        from bs4 import Comment
        comments = soup.find_all(string=lambda t: isinstance(t, Comment))
        for c in comments:
            if 'id="games"' in c:
                table = BeautifulSoup(c, 'html.parser').find('table', id='games')
                break
    rows = table.select('tbody tr') if table else []

    games = []
    for row in rows:
        if 'thead' in row.get('class', []):
            continue
        date_cell = row.find('th', {'data-stat': 'date_game'})
        if not date_cell or not date_cell.a:
            continue
        date = date_cell.text.strip()
        box_score_link = row.find('a', text='Box Score')
        opp = row.find('td', {'data-stat': 'opp_name'}).get_text(strip=True)
        loc_flag = row.find('td', {'data-stat': 'game_location'}).get_text(strip=True)
        home_away = 'away' if loc_flag == '@' else 'home'

        if box_score_link:
            href = box_score_link['href']
            game_id = href.split('/')[-1].replace('.html', '')
            games.append({
                'date': date,
                'opponent': opp,
                'location': home_away,
                'box_score_url': f"{BASE_URL}{href}",
                'file': f"{game_id}.json"
            })
    return games


def fetch_box_score(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    tables = {}
    for table in soup.select('table'):  # capture all tables
        table_id = table.get('id')
        if not table_id:
            continue
        headers = [th.get_text(strip=True) for th in table.select('thead tr th')]
        rows = []
        for tr in table.select('tbody tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['th', 'td'])]
            rows.append(cells)
        tables[table_id] = {
            'headers': headers,
            'rows': rows
        }
    return tables


def main():
    games = fetch_schedule()
    with open(os.path.join(DATA_DIR, 'games.json'), 'w') as f:
        json.dump(games, f, indent=2)
    for game in games:
        data = fetch_box_score(game['box_score_url'])
        with open(os.path.join(BOX_DIR, game['file']), 'w') as f:
            json.dump(data, f, indent=2)
    print(f"Saved {len(games)} games to {DATA_DIR}")


if __name__ == '__main__':
    main()
