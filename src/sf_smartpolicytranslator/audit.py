"""SQLite audit trail + policy persistence (stdlib). Point PLT_SQLITE_PATH
elsewhere for a shared DB; never overwrites audit rows."""
from __future__ import annotations
import json, os, sqlite3, time, uuid
_DB = os.environ.get("SPT_SQLITE_PATH",
                     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                         os.path.abspath(__file__)))), "spt.db"))


def _c():
    c = sqlite3.connect(_DB)
    c.execute("CREATE TABLE IF NOT EXISTS policies(id TEXT PRIMARY KEY, source TEXT, policy TEXT, valid INT, created_at REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS audit(id TEXT PRIMARY KEY, action TEXT, target TEXT, payload TEXT, ts REAL)")
    return c


def save_policy(pid, source, policy, valid):
    c = _c(); c.execute("INSERT OR REPLACE INTO policies VALUES(?,?,?,?,?)",
                        (pid, source[:200], json.dumps(policy), int(valid), time.time()))
    c.commit(); c.close(); log("save_policy", pid, {"valid": valid})


def get_policy(pid):
    c = _c(); r = c.execute("SELECT policy FROM policies WHERE id=?", (pid,)).fetchone(); c.close()
    return json.loads(r[0]) if r else None


def log(action, target="", payload=None):
    c = _c(); c.execute("INSERT INTO audit VALUES(?,?,?,?,?)",
                        (str(uuid.uuid4()), action, target, json.dumps(payload or {}), time.time()))
    c.commit(); c.close()


def audit_trail(limit=100):
    c = _c(); rows = c.execute("SELECT id,action,target,payload,ts FROM audit ORDER BY ts DESC LIMIT ?", (limit,)).fetchall(); c.close()
    return [{"id": r[0], "action": r[1], "target": r[2], "payload": json.loads(r[3]), "ts": r[4]} for r in rows]
