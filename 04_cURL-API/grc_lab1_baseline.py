from http.server import HTTPServer, BaseHTTPRequestHandler
import json, re, secrets, hashlib, hmac, time

users = {}
sessions = {}
posts = {}
next_post_id = 1

SESSION_COOKIE_NAME = "session"
SESSION_TTL_SECONDS = 60 * 60

def jdump(obj) -> bytes:
    return json.dumps(obj, indent=2).encode()

def now() -> int:
    return int(time.time())

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()

def parse_cookie(cookie_header: str) -> dict:
    if not cookie_header:
        return {}
    out = {}
    for part in cookie_header.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def get_session_id(headers):
    cookies = parse_cookie(headers.get("Cookie", ""))
    return cookies.get(SESSION_COOKIE_NAME)

def is_session_valid(sid: str) -> bool:
    if not sid or sid not in sessions:
        return False
    if now() - sessions[sid]["created"] > SESSION_TTL_SECONDS:
        sessions.pop(sid, None)
        return False
    return True

def require_auth(handler):
    sid = get_session_id(handler.headers)
    if not is_session_valid(sid):
        handler._send(401, {"error": "unauthenticated"})
        return None
    return sessions[sid]["username"]

def require_admin(handler, username: str) -> bool:
    if users.get(username, {}).get("role") != "admin":
        handler._send(403, {"error": "forbidden"})
        return False
    return True

class H(BaseHTTPRequestHandler):
    def _read_json(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) if n else b""
        if not raw:
            return None
        try:
            return json.loads(raw.decode())
        except Exception:
            return {"_raw": raw.decode(errors="replace")}

    def _send(self, code: int, obj=None, extra_headers=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        if obj is not None:
            self.wfile.write(jdump(obj))

    def do_GET(self):
        if self.path == "/":
            return self._send(200, {
                "message": "GRC Lab 1 baseline API",
                "routes": ["/register", "/login", "/logout", "/me", "/api/posts", "/api/posts/<id>", "/admin"]
            })

        if self.path == "/me":
            username = require_auth(self)
            if not username:
                return
            return self._send(200, {"username": username, "role": users[username]["role"]})

        if re.fullmatch(r"/api/posts/?", self.path):
            username = require_auth(self)
            if not username:
                return
            mine = [p for p in posts.values() if p["owner"] == username]
            return self._send(200, {"posts": mine})

        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if m:
            username = require_auth(self)
            if not username:
                return
            pid = int(m.group(1))
            if pid not in posts:
                return self._send(404, {"error": "not found"})
            if posts[pid]["owner"] != username:
                return self._send(403, {"error": "forbidden"})
            return self._send(200, posts[pid])

        if self.path == "/admin":
            username = require_auth(self)
            if not username:
                return
            if not require_admin(self, username):
                return
            return self._send(200, {
                "admin": True,
                "users": [{"username": u["username"], "role": u["role"]} for u in users.values()],
                "post_count": len(posts)
            })

        return self._send(404, {"error": "unknown route"})

    def do_POST(self):
        global next_post_id

        if self.path == "/register":
            data = self._read_json() or {}
            username = (data.get("username") or "").strip()
            password = (data.get("password") or "")
            if not username or not password:
                return self._send(400, {"error": "username and password required"})
            if username in users:
                return self._send(409, {"error": "user already exists"})

            salt = secrets.token_hex(8)
            pw_hash = hash_password(password, salt)
            role = "admin" if username == "admin" else "user"
            users[username] = {"username": username, "salt": salt, "pw_hash": pw_hash, "role": role}
            return self._send(201, {"created": True, "username": username, "role": role})

        if self.path == "/login":
            data = self._read_json() or {}
            username = (data.get("username") or "").strip()
            password = (data.get("password") or "")
            if username not in users:
                return self._send(401, {"error": "invalid credentials"})

            salt = users[username]["salt"]
            expected = users[username]["pw_hash"]
            got = hash_password(password, salt)
            if not hmac.compare_digest(expected, got):
                return self._send(401, {"error": "invalid credentials"})

            sid = secrets.token_urlsafe(24)
            sessions[sid] = {"username": username, "created": now()}
            cookie = f"{SESSION_COOKIE_NAME}={sid}; Path=/; HttpOnly"
            return self._send(200, {"login": "ok"}, {"Set-Cookie": cookie})

        if self.path == "/logout":
            sid = get_session_id(self.headers)
            if sid in sessions:
                sessions.pop(sid, None)
            cookie = f"{SESSION_COOKIE_NAME}=deleted; Path=/; Max-Age=0"
            return self._send(200, {"logout": "ok"}, {"Set-Cookie": cookie})

        if re.fullmatch(r"/api/posts/?", self.path):
            username = require_auth(self)
            if not username:
                return
            data = self._read_json() or {}
            pid = next_post_id
            next_post_id += 1
            posts[pid] = {
                "id": pid,
                "owner": username,
                "title": data.get("title") or "",
                "body": data.get("body") or ""
            }
            return self._send(201, posts[pid], {"Location": f"/api/posts/{pid}"})

        return self._send(404, {"error": "unknown route"})

    def do_PATCH(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        username = require_auth(self)
        if not username:
            return
        pid = int(m.group(1))
        if pid not in posts:
            return self._send(404, {"error": "not found"})
        if posts[pid]["owner"] != username:
            return self._send(403, {"error": "forbidden"})

        data = self._read_json() or {}
        if "title" in data:
            posts[pid]["title"] = data["title"]
        if "body" in data:
            posts[pid]["body"] = data["body"]
        return self._send(200, posts[pid])

    def do_PUT(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        username = require_auth(self)
        if not username:
            return
        pid = int(m.group(1))
        if pid not in posts:
            return self._send(404, {"error": "not found"})
        if posts[pid]["owner"] != username:
            return self._send(403, {"error": "forbidden"})

        data = self._read_json() or {}
        posts[pid] = {"id": pid, "owner": username, "title": data.get("title") or "", "body": data.get("body") or ""}
        return self._send(200, posts[pid])

    def do_DELETE(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        username = require_auth(self)
        if not username:
            return
        pid = int(m.group(1))
        if pid not in posts:
            return self._send(404, {"error": "not found"})
        if posts[pid]["owner"] != username:
            return self._send(403, {"error": "forbidden"})
        deleted = posts.pop(pid)
        return self._send(200, {"deleted": deleted})

def main():
    print("GRC Lab 1 baseline listening on http://127.0.0.1:8080")
    HTTPServer(("127.0.0.1", 8080), H).serve_forever()

if __name__ == "__main__":
    main()
