import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function Game() {
  const { id } = useParams();
  const [box, setBox] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/api/boxscore/${id}`)
      .then(res => res.json())
      .then(data => setBox(data));
  }, [id]);

  if (!box) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <Link to="/">← Back to schedule</Link>
      <h1>Box Score</h1>
      {['away', 'home'].map(side => (
        <div key={side} style={{ marginTop: '2rem' }}>
          <h2>{side.toUpperCase()}</h2>
          <table border="1" cellPadding="5">
            <thead>
              <tr><th>Player</th><th>MIN</th><th>PTS</th><th>REB</th><th>AST</th><th>STL</th><th>BLK</th><th>TO</th><th>FG%</th></tr>
            </thead>
            <tbody>
              {box[side].map((p, i) => (
                <tr key={i}>
                  <td>{p.player}</td><td>{p.min}</td><td>{p.pts}</td><td>{p.reb}</td><td>{p.ast}</td><td>{p.stl}</td><td>{p.blk}</td><td>{p.turnover}</td><td>{(p.fg_pct * 100).toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
