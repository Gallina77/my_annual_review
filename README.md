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

## One-click start
Double-click `start.command` (Mac) or `start.bat` (Windows). The first time on a Mac, right-click the file, choose Open and confirm once. If it will not run, execute `chmod +x start.command` in Terminal one time. If the workbook is already running, the launcher just opens it again in your browser.

## Mac app
`Annual Review.app` (wheel icon) does the same as `start.command`. Keep it inside this folder. To put it on the Desktop or Dock, right-click it and choose Make Alias, or drag it onto the Dock.
First start: right-click the app, choose Open and confirm once. If macOS still refuses (files copied from a downloaded zip carry a quarantine flag), run this once in Terminal inside the folder:
```
xattr -dr com.apple.quarantine .
chmod +x start.command "Annual Review.app/Contents/MacOS/launcher"
```
Your data stays in `annual_review.db` in this folder, whichever way you start it.

## Without the server
Open `index.html` directly. Answers then save in the browser (localStorage and IndexedDB) on this device only.

## Features
- Wheel as progress map, one workspace per step.
- **Digital / Paper / Both** per step: work in your notebook, then add photos of your pages and the lines worth keeping. Photos are resized in the browser and stored in the same local database.
- **Linking between steps**: gratitude items, excitement topics, portrait lines and resonance-log entries can be pulled into the project board (as "Ideas to sort"), the portrait step and the annual letter.
- **Focus timer** under the wheel (25/50/90 minute blocks with breaks). Focus time is logged per phase against the template's 8-hour plan.
- **Recap** button: a one-page card with your word of the year, top gratitudes, chosen projects and principles. Copy it as text or save it as a file.
- **Favourite gratitudes**: star the items that mean most. The recap shows starred items first.
- **Start next year's review** (in Versions or the Recap): saves this review as a version, clears the workbook, and shows last year's highlights in the first steps. Photos stay with the review they belong to.
- **Versions** button: save named snapshots (for example one per year) and restore them.
- **Backup file**: download or import all answers and versions as one JSON file.

## Credits and license note
The wheel and its steps come from Tiago Forte's *Life in Perspective* and the Annual Life Review Template (Forte Labs), which is licensed for personal, non-commercial use. The prompts here are shortened and reworded from that template. Keep this repository **private** and do not redistribute.
