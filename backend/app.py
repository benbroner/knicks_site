from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
API_BASE = "https://www.balldontlie.io/api/v1"
TEAM_ID = 14  # Knicks team ID

@app.route('/api/schedule')
def schedule():
    # Return all Knicks games in 2024 calendar year
    params = {
        'team_ids[]': TEAM_ID,
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'per_page': 100
    }
    resp = requests.get(f"{API_BASE}/games", params=params)
    data = resp.json()['data']
    # Map to simplified structure
    games = []
    for g in data:
        games.append({
            'id': g['id'],
            'date': g['date'][:10],  # YYYY-MM-DD
            'home_team': g['home_team']['full_name'],
            'visitor_team': g['visitor_team']['full_name'],
            'home_score': g['home_team_score'],
            'visitor_score': g['visitor_team_score']
        })
    return jsonify(games)

@app.route('/api/boxscore/<int:game_id>')
def boxscore(game_id):
    # Fetch stats for a given game
    params = {
        'game_ids[]': game_id,
        'per_page': 100
    }
    resp = requests.get(f"{API_BASE}/stats", params=params)
    stats = resp.json()['data']
    # Group stats by team
    box = {'home': [], 'away': []}
    # Also fetch game meta to know which is home vs visitor
    game = requests.get(f"{API_BASE}/games/{game_id}").json()
    home_id = game['home_team']['id']
    for s in stats:
        entry = {
            'player': s['player']['first_name'] + ' ' + s['player']['last_name'],
            'pts': s['pts'],
            'reb': s['reb'],
            'ast': s['ast'],
            'stl': s['stl'],
            'blk': s['blk'],
            'turnover': s['turnover'],
            'fg_pct': s['fg_pct'],
            'min': s['min']
        }
        if s['team']['id'] == home_id:
            box['home'].append(entry)
        else:
            box['away'].append(entry)
    return jsonify(box)

if __name__ == '__main__':
    print(app.url_map)            # lists all defined routes
    app.run(port=5000, debug=True)
