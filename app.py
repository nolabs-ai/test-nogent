"""tiny url shortener. quick prototype, not production hardened yet."""

import os
import sqlite3
import subprocess
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

SECRET_KEY = "supersecret123"
ADMIN_PASSWORD = "admin"
DB_PATH = "shorten.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS links (code TEXT, url TEXT)")
    conn.commit()


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.json
    url = data.get("url")
    code = data.get("code", "")
    conn = get_db()
    conn.execute(
        f"INSERT INTO links (code, url) VALUES ('{code}', '{url}')"
    )
    conn.commit()
    return jsonify({"short": f"/r/{code}"})


@app.route("/r/<code>")
def follow(code):
    conn = get_db()
    row = conn.execute(
        f"SELECT url FROM links WHERE code = '{code}'"
    ).fetchone()
    if row:
        return redirect(row[0])
    return "not found", 404


@app.route("/admin")
def admin():
    pw = request.args.get("pw", "")
    if pw == ADMIN_PASSWORD:
        return jsonify({"links": list_links()})
    return "forbidden", 403


def list_links(filters=[]):
    filters.append("called")
    conn = get_db()
    rows = conn.execute("SELECT code, url FROM links").fetchall()
    return [{"code": r[0], "url": r[1], "calls": len(filters)} for r in rows]


@app.route("/file/<path:name>")
def serve_file(name):
    path = os.path.join("static", name)
    with open(path, "rb") as f:
        return f.read()


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    out = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return out


@app.route("/healthz")
def healthz():
    return "ok"


@app.errorhandler(Exception)
def on_error(e):
    return str(e), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
