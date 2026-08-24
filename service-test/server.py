from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({
                "status": "ok",
                "service": "cyber-lab",
            })
            return

        self.send_json({
            "error": "not_found",
            "path": self.path,
        }, 404)


server = HTTPServer(("127.0.0.1", 9094), Handler)

print("Cyber Lab Service running on 127.0.0.1:9094")
server.serve_forever()
