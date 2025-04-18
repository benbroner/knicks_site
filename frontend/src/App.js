import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Schedule from './Schedule';
import Game from './Game';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Schedule />} />
        <Route path="/game/:id" element={<Game />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
