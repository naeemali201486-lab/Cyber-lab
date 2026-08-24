from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.request import urlopen
import json
import time


class Handler(SimpleHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/status":
            start = time.perf_counter()

            try:
                with urlopen(
                    "http://127.0.0.1:9094/health",
                    timeout=3
                ) as response:
                    body = json.loads(response.read().decode())
                    elapsed = (time.perf_counter() - start) * 1000

                self.send_json({
                    "status": "online",
                    "service": body.get("service"),
                    "response_ms": round(elapsed, 2),
                })
            except Exception:
                self.send_json({
                    "status": "offline",
                    "service": "cyber-lab",
                }, 503)
            return

        super().do_GET()


server = HTTPServer(("127.0.0.1", 9095), Handler)

print("Cyber Lab Dashboard running on 127.0.0.1:9095")
server.serve_forever()
