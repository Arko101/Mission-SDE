#!/usr/bin/env python3
"""Zero-dependency local-first study dashboard server, backed by SQLite.
Run: python server.py
Data lives in study_progress.sqlite3, never browser localStorage.
"""
from __future__ import annotations
import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get('STUDY_DB', str(ROOT / 'study_progress.sqlite3'))).resolve()
HOST = os.environ.get('STUDY_HOST', '127.0.0.1')
PORT = int(os.environ.get('STUDY_PORT', '8765'))
MAX_BODY = 256 * 1024


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def connect():
    cx = sqlite3.connect(DB, timeout=15)
    cx.row_factory = sqlite3.Row
    cx.execute('PRAGMA busy_timeout=15000')
    return cx


def initialize():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as cx:
        cx.execute('PRAGMA journal_mode=WAL')
        cx.execute('''CREATE TABLE IF NOT EXISTS task_progress (
            task_id TEXT PRIMARY KEY, completed INTEGER NOT NULL CHECK (completed IN (0,1)),
            updated_at TEXT NOT NULL)''')
        cx.execute('''CREATE TABLE IF NOT EXISTS week_notes (
            week_id TEXT PRIMARY KEY, note TEXT NOT NULL,
            updated_at TEXT NOT NULL)''')
        cx.execute('''CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, company TEXT NOT NULL,
            role TEXT NOT NULL, stage TEXT NOT NULL, notes TEXT NOT NULL)''')
        cx.execute('''CREATE TABLE IF NOT EXISTS interview_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            round_type TEXT NOT NULL,
            result TEXT NOT NULL,
            reflection TEXT NOT NULL)''')


def read_state():
    with connect() as cx:
        return {
            'progress': {r['task_id']: bool(r['completed']) for r in cx.execute('SELECT task_id,completed FROM task_progress')},
            'notes': {r['week_id']: r['note'] for r in cx.execute('SELECT week_id,note FROM week_notes')},
            'interviews': [dict(r) for r in cx.execute('SELECT id,created_at,round_type,result,reflection FROM interview_logs ORDER BY id DESC')],
            'applications': [dict(r) for r in cx.execute('SELECT id,created_at,company,role,stage,notes FROM applications ORDER BY id DESC')],
            'database': 'SQLite on server',
        }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Avoid stale state, and never permit cross-origin API requests.
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        super().end_headers()

    def reply(self, status, payload, extra_headers=None):
        body = json.dumps(payload, ensure_ascii=False).encode('utf8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        for key, val in (extra_headers or {}).items():
            self.send_header(key, val)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path).path
        if url == '/api/state':
            return self.reply(200, read_state())
        if url == '/api/export':
            return self.reply(200, {'exported_at': now(), **read_state()},
                              {'Content-Disposition':'attachment; filename="sde-progress-backup.json"'})
        if url.startswith('/api/'):
            return self.reply(404, {'error':'Unknown endpoint'})
        if url in ('/', '/index.html', '/styles.css', '/app.js', '/roadmap.json'):
            return super().do_GET()
        return self.reply(404, {'error':'Not found'})

    def do_POST(self):
        url = urlparse(self.path).path
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > MAX_BODY:
                return self.reply(413, {'error':'Invalid request size'})
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                return self.reply(400, {'error':'Expected a JSON object'})
            if url == '/api/task':
                key = payload.get('id')
                completed = payload.get('completed')
                if not isinstance(key, str) or not 1 <= len(key) <= 140 or not isinstance(completed, bool):
                    return self.reply(400, {'error':'Invalid task data'})
                with connect() as cx:
                    cx.execute('INSERT INTO task_progress(task_id, completed, updated_at) VALUES (?,?,?) '
                               'ON CONFLICT(task_id) DO UPDATE SET completed=excluded.completed, updated_at=excluded.updated_at',
                               (key, int(completed), now()))
                return self.reply(200, {'ok':True})
            if url == '/api/note':
                key, note = payload.get('week_id'), payload.get('note')
                if not isinstance(key, str) or not 1 <= len(key) <= 80 or not isinstance(note,str) or len(note) > 12000:
                    return self.reply(400, {'error':'Invalid note'})
                with connect() as cx:
                    cx.execute('INSERT INTO week_notes(week_id, note, updated_at) VALUES (?,?,?) '
                               'ON CONFLICT(week_id) DO UPDATE SET note=excluded.note,updated_at=excluded.updated_at',
                               (key, note, now()))
                return self.reply(200, {'ok':True})
            if url == '/api/interview':
                kind, result, reflection = (payload.get('round_type'),payload.get('result'),payload.get('reflection'))
                if not isinstance(kind,str) or len(kind)>50 or not kind or not isinstance(result,str) or len(result)>50 or not result or not isinstance(reflection,str) or len(reflection)>6000:
                    return self.reply(400,{'error':'Invalid interview log'})
                with connect() as cx:
                    cursor=cx.execute('INSERT INTO interview_logs(created_at,round_type,result,reflection) VALUES (?,?,?,?)', (now(),kind,result,reflection))
                    entry_id=cursor.lastrowid
                return self.reply(200, {'ok':True,'id':entry_id})
            if url == '/api/application':
                company, role, stage, notes = (payload.get('company'),payload.get('role'),payload.get('stage'),payload.get('notes',''))
                if not all(isinstance(x,str) for x in (company,role,stage,notes)) or not 1 <= len(company) <= 100 or not 1 <= len(role) <= 140 or stage not in ('Saved','Applied','Referral','Recruiter','Interview','Offer','Rejected') or len(notes)>2500:
                    return self.reply(400, {'error':'Invalid application data'})
                with connect() as cx:
                    cursor = cx.execute('INSERT INTO applications(created_at,company,role,stage,notes) VALUES (?,?,?,?,?)',(now(),company,role,stage,notes))
                return self.reply(200, {'ok':True, 'id':cursor.lastrowid})
            if url == '/api/application/update':
                id_,stage=payload.get('id'),payload.get('stage')
                if not isinstance(id_,int) or stage not in ('Saved','Applied','Referral','Recruiter','Interview','Offer','Rejected'):
                    return self.reply(400,{'error':'Invalid update'})
                with connect() as cx:
                    cx.execute('UPDATE applications SET stage=? WHERE id=?',(stage,id_))
                return self.reply(200,{'ok':True})
            if url == '/api/import':
                state = payload.get('state')
                if not isinstance(state, dict) or not isinstance(state.get('progress'),dict) or not isinstance(state.get('notes'),dict):
                    return self.reply(400, {'error':'Invalid backup shape'})
                tasks, notes = state['progress'], state['notes']
                if len(tasks)>3000 or len(notes)>300 or sum(len(str(v)) for v in notes.values())>200000:
                    return self.reply(413, {'error':'Backup is too large'})
                for k,v in tasks.items():
                    if not isinstance(k,str) or len(k)>140 or not isinstance(v,bool):
                        return self.reply(400, {'error':'Invalid backup tasks'})
                for k,v in notes.items():
                    if not isinstance(k,str) or len(k)>80 or not isinstance(v,str) or len(v)>12000:
                        return self.reply(400, {'error':'Invalid backup notes'})
                with connect() as cx:
                    cx.execute('DELETE FROM task_progress')
                    cx.execute('DELETE FROM week_notes')
                    cx.executemany('INSERT INTO task_progress(task_id,completed,updated_at) VALUES (?,?,?)', [(k,int(v),now()) for k,v in tasks.items()])
                    cx.executemany('INSERT INTO week_notes(week_id,note,updated_at) VALUES (?,?,?)', [(k,v,now()) for k,v in notes.items()])
                return self.reply(200, {'ok':True})
            return self.reply(404, {'error':'Unknown endpoint'})
        except (json.JSONDecodeError,UnicodeDecodeError, ValueError):
            return self.reply(400, {'error':'Invalid JSON'})
        except (BrokenPipeError,ConnectionResetError):
            return
        except sqlite3.Error as exc:
            self.log_error('Database error: %s', exc)
            return self.reply(500, {'error':'Database operation failed'})


if __name__ == '__main__':
    initialize()
    print(f'\nSDE Mission Control is running at http://{HOST}:{PORT}\nData saved in: {DB}\nPress Ctrl+C to stop.\n')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
