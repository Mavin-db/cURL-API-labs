from http.server import HTTPServer, BaseHTTPRequestHandler
import json, re

posts = {}
next_id = 1
API_TOKEN = "password123"

def jdump(obj) -> bytes:
    return json.dumps(obj, indent=2).encode()

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

    def _send(self, code: int, obj=None, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        if obj is not None:
            self.wfile.write(jdump(obj))

    def _require_token(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            self._send(401, {"error": "missing token", "hint": "Authorization: Bearer <token>"})
            return False
        token = auth.split(" ", 1)[1].strip()
        if token != API_TOKEN:
            self._send(403, {"error": "invalid token"})
            return False
        return True

    def do_GET(self):
        if re.fullmatch(r"/api/posts/?", self.path):
            return self._send(200, {"posts": list(posts.values())})
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if m:
            pid = int(m.group(1))
            if pid not in posts:
                return self._send(404, {"error": "not found"})
            return self._send(200, posts[pid])
        return self._send(404, {"error": "unknown route"})

    def do_POST(self):
        global next_id
        if not re.fullmatch(r"/api/posts/?", self.path):
            return self._send(404, {"error": "unknown route"})
        if not self._require_token():
            return
        data = self._read_json() or {}
        pid = next_id
        next_id += 1
        posts[pid] = {"id": pid, **data}
        return self._send(201, posts[pid], {"Location": f"/api/posts/{pid}"})

    def do_PATCH(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        if not self._require_token():
            return
        pid = int(m.group(1))
        if pid not in posts:
            return self._send(404, {"error": "not found"})
        data = self._read_json() or {}
        posts[pid].update(data)
        return self._send(200, posts[pid])

    def do_PUT(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        if not self._require_token():
            return
        pid = int(m.group(1))
        data = self._read_json() or {}
        posts[pid] = {"id": pid, **data}
        return self._send(200, posts[pid])

    def do_DELETE(self):
        m = re.fullmatch(r"/api/posts/(\d+)/?", self.path)
        if not m:
            return self._send(404, {"error": "unknown route"})
        if not self._require_token():
            return
        pid = int(m.group(1))
        if pid not in posts:
            return self._send(404, {"error": "not found"})
        deleted = posts.pop(pid)
        return self._send(200, {"deleted": deleted})

def main():
    print("Token auth API listening on http://127.0.0.1:8080")
    print("Token is:", API_TOKEN)
    HTTPServer(("127.0.0.1", 8080), H).serve_forever()

if __name__ == "__main__":
    main()
