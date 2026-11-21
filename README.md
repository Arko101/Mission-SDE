
# SDE Mission Control

A playful, interactive **27-week software-engineering interview preparation dashboard** 
=======
# SDE Mission Control

A playful, interactive **27-week software-engineering interview preparation dashboard** .
>>>>>>> 179886c (refactored folder)

**Persistence:** A Python standard-library backend + **SQLite**. No localStorage, sessionStorage, IndexedDB, or browser-based persistence.

## Quick start

1. Install Python 3.9+.
2. Extract the zip and open a terminal inside `sde-study-command-center`.
3. Run `python server.py` (on Windows `py server.py` also works).
4. Open **http://127.0.0.1:8765** in your browser.

Stop the backend with Ctrl+C. Start it again any time and your saved progress will remain.

**Do not double-click index.html and open it as a file:// page.** Saving requires the running backend.

## Features

- 27 weeks: Dometrain chapter/exercises → selected Educative patterns → independent LeetCode C# problems.
- Friday/Saturday system design + CS labs; Sunday DSA revision and CounterNet.
- Checkboxes, XP, week/phase progress, optional stretch labels, filters, search, and direct problem links.
- Auto-saved weekly notes, interview reflection journal, application tracker, and milestone views.
- JSON progress export. Import restores checkmarks and weekly notes; to restore *all* data, retain the SQLite database.
- Responsive UI with no frontend build tools, external JS libraries, or extra Python packages.

## Your persistent data

The first launch creates **study_progress.sqlite3** in this folder. Back it up periodically (stop the server before copying the file, so SQLite writes are fully checkpointed). The **Backup progress** button also exports JSON of tasks, notes, interview logs and applications.

To move to another computer, copy this folder including the SQLite database. To access the same data across devices, you must host the backend securely. By default, it binds only to **127.0.0.1**.

## Important security note

This is a **single-user app with no login system**. Do not expose it publicly. Binding `STUDY_HOST=0.0.0.0` or deploying to the public internet without authentication and HTTPS would reveal and allow changes to your study data.

## Files

- `index.html`: dashboard entry point
- `styles.css`: design and responsive styling
- `app.js`: interactive UI and backend saving
- `roadmap.json`: dated curriculum and links
- `server.py`: minimal server + SQLite endpoints
- `build_data.py`: regenerates `roadmap.json` from the editable study plan
- `study_progress.sqlite3`: automatically created on launch; **do not delete your database when updating the app**

## Progress integrity

Tasks and notes are stored on the backend. When the server cannot save a checkbox, the UI reverts the checkmark rather than falsely claiming success. Course pages and lesson names can change; use the named Educative pattern/example within the linked course.

## Study philosophy

- DSA exercises: attempt independently in C# before viewing help or using AI.
- Revisit difficult problems after about 2 days, 1 week and 3 weeks.
- Friday/Saturday are for system design; Sunday is review plus a small CounterNet session.
- Begin targeted applications in April, and resign only after receiving a suitable written offer.
