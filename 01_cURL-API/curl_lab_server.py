from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class H(BaseHTTPRequestHandler):
    def _read_body(self) -> bytes:
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n) if n else b""

    def _send(self, code: int = 200, obj=None, extra_headers=None) -> None:
        body = b""
        if obj is not None:
            body = json.dumps(obj, indent=2).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()

        if body:
            self.wfile.write(body)

    def _reply(self, method: str) -> None:
        body = self._read_body()
        try:
            body_json = json.loads(body.decode()) if body else None
        except Exception:
            body_json = {"_raw": body.decode(errors="replace")}

        self._send(200, {
            "method": method,
            "path": self.path,
            "headers": {k: v for k, v in self.headers.items()},
            "body": body_json
        })

    def do_GET(self) -> None:
        if self.path.startswith("/redirect"):
            self._send(302, {"msg": "redirecting"}, {"Location": "/get"})
            return

        if self.path.startswith("/status/"):
            code = int(self.path.split("/status/")[1].split("?")[0])
            self._send(code, {"status": code})
            return

        if self.path.startswith("/cookie/set"):
            self._send(200, {"set": "session=123"}, {"Set-Cookie": "session=123; Path=/"})
            return

        self._reply("GET")

    def do_POST(self) -> None: self._reply("POST")
    def do_PUT(self) -> None: self._reply("PUT")
    def do_PATCH(self) -> None: self._reply("PATCH")
    def do_DELETE(self) -> None: self._reply("DELETE")

def main() -> None:
    print("Listening on http://127.0.0.1:8080")
    HTTPServer(("127.0.0.1", 8080), H).serve_forever()

if __name__ == "__main__":
    main()
