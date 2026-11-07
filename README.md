# My Annual Review

A personal, interactive workbook for the yearly review, built around the twelve-step Annual Review wheel.

## Run it with a local database (recommended)
Needs Python 3 only (preinstalled on most Macs; no packages to install).

```
python3 server.py
```

It opens http://localhost:8765. Your answers, photos and versions are stored in `annual_review.db` (SQLite) next to the script.
The server listens on 127.0.0.1 only, and the database file is excluded from git, so your answers never leave your computer or end up in the repo.
Stop it with Ctrl+C. Your data stays in the file. Back it up by copying `annual_review.db`.

## Without the server
Open `index.html` directly. Answers then save in the browser (localStorage and IndexedDB) on this device only.

## Features
- Wheel as progress map, one workspace per step.
- **Digital / Paper / Both** per step: work in your notebook, then add photos of your pages and the lines worth keeping. Photos are resized in the browser and stored in the same local database.
- **Versions** button: save named snapshots (for example one per year) and restore them.
- **Backup file**: download or import all answers and versions as one JSON file.

## Credits and license note
The wheel and its steps come from Tiago Forte's *Life in Perspective* and the Annual Life Review Template (Forte Labs), which is licensed for personal, non-commercial use. The prompts here are shortened and reworded from that template. Keep this repository **private** and do not redistribute.
