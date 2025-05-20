# Knicks Site

This repository will house the code for the Knicks site.


## Usage

1. **Download box scores** (requires internet access):
   ```bash
   python scripts/download_box_scores.py
   ```
   This will create `data/games.json` and one JSON file per game inside `data/box_scores/`.

2. **View website**:
   Use a simple HTTP server to serve the `site` directory:
   ```bash
   cd site
   python -m http.server 8000
   ```
   Then open `http://localhost:8000/index.html` in your browser.

The current repository includes placeholder data for two games as an example.
