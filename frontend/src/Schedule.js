import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function Schedule() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/schedule')
      .then(res => res.json())
      .then(data => setGames(data));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Knicks 2024 Schedule</h1>
      <ul>
        {games.map(g => (
          <li key={g.id} style={{ marginBottom: '1rem' }}>
            <Link to={`/game/${g.id}`}>
              {g.date}: {g.visitor_team} @ {g.home_team} — {g.visitor_score}–{g.home_score}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
