#!/usr/bin/env python3
"""Local server for My Annual Review: serves index.html and stores answers in a SQLite file.

Run:  python3 server.py      then open http://localhost:8765
Your data lives in annual_review.db next to this file. It never leaves your computer
(the server only listens on 127.0.0.1) and is excluded from git.
"""
import json, os, sqlite3, sys, threading, time, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "annual_review.db")
PORT = int(os.environ.get("PORT", "8765"))
MAX = 25 * 1024 * 1024
LOCK = threading.Lock()


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


with conn() as c:
    c.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK (id = 1), ts INTEGER, json TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS photos (id TEXT PRIMARY KEY, ts INTEGER, step INTEGER, json TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS snaps (id TEXT PRIMARY KEY, ts INTEGER, name TEXT, json TEXT NOT NULL)")


class H(BaseHTTPRequestHandler):
    server_version = "AnnualReview/1"

    def log_message(self, *a):
        pass

    def _ok_host(self):
        host = (self.headers.get("Host") or "").split(":")[0]
        if host not in ("localhost", "127.0.0.1"):
            return False
        origin = self.headers.get("Origin")
        if origin and origin.split("://")[-1].split(":")[0] not in ("localhost", "127.0.0.1"):
            return False
        return True

    def _send(self, code, body=b"", ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX:
            raise ValueError("too large")
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        if not self._ok_host():
            return self._send(403)
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if p == "/api/state":
            with conn() as c:
                r = c.execute("SELECT json FROM state WHERE id = 1").fetchone()
            return self._send(200, r["json"].encode() if r else b"{}")
        if p == "/api/snaps":
            with conn() as c:
                rows = c.execute("SELECT json FROM snaps ORDER BY ts DESC").fetchall()
            return self._send(200, ("[" + ",".join(r["json"] for r in rows) + "]").encode())
        if p == "/api/photos":
            with conn() as c:
                rows = c.execute("SELECT json FROM photos ORDER BY ts").fetchall()
            return self._send(200, ("[" + ",".join(r["json"] for r in rows) + "]").encode())
        self._send(404)

    def do_PUT(self):
        if not self._ok_host():
            return self._send(403)
        if self.path.split("?")[0] != "/api/state":
            return self._send(404)
        try:
            d = self._body()
            assert isinstance(d, dict) and isinstance(d.get("v"), dict)
        except Exception:
            return self._send(400, {"error": "bad request"})
        with LOCK, conn() as c:
            c.execute("INSERT OR REPLACE INTO state (id, ts, json) VALUES (1, ?, ?)", (int(d.get("ts") or time.time() * 1000), json.dumps(d)))
        self._send(200, {"ok": True})

    def do_POST(self):
        if not self._ok_host():
            return self._send(403)
        path = self.path.split("?")[0]
        if path == "/api/photos":
            try:
                d = self._body()
                assert isinstance(d.get("id"), str) and isinstance(d.get("data"), str) and d["data"].startswith("data:image/")
            except Exception:
                return self._send(400, {"error": "bad request"})
            with LOCK, conn() as c:
                c.execute("INSERT OR REPLACE INTO photos (id, ts, step, json) VALUES (?, ?, ?, ?)", (d["id"], int(d.get("ts") or 0), int(d.get("step") or 0), json.dumps(d)))
            return self._send(200, {"ok": True})
        if path != "/api/snaps":
            return self._send(404)
        try:
            d = self._body()
            assert isinstance(d.get("id"), str) and isinstance(d.get("data"), dict)
        except Exception:
            return self._send(400, {"error": "bad request"})
        with LOCK, conn() as c:
            c.execute("INSERT OR REPLACE INTO snaps (id, ts, name, json) VALUES (?, ?, ?, ?)", (d["id"], int(d.get("ts") or 0), str(d.get("name", "")), json.dumps(d)))
        self._send(200, {"ok": True})

    def do_DELETE(self):
        if not self._ok_host():
            return self._send(403)
        p = self.path.split("?")[0]
        if p.startswith("/api/photos/"):
            with LOCK, conn() as c:
                c.execute("DELETE FROM photos WHERE id = ?", (p.rsplit("/", 1)[1],))
            return self._send(200, {"ok": True})
        if not p.startswith("/api/snaps/"):
            return self._send(404)
        with LOCK, conn() as c:
            c.execute("DELETE FROM snaps WHERE id = ?", (p.rsplit("/", 1)[1],))
        self._send(200, {"ok": True})


if __name__ == "__main__":
    url = "http://localhost:%d" % PORT
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    except OSError:
        print("Port %d is already in use. The workbook is probably already running." % PORT)
        print("Opening it in your browser:", url)
        if "--no-open" not in sys.argv:
            webbrowser.open(url)
        sys.exit(0)
    print("My Annual Review running at", url)
    print("Database file:", DB)
    print("Press Ctrl+C to stop.")
    if "--no-open" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
