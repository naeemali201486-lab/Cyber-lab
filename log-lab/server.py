from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

LOG_FILE = "access.log"


def write_log(method, path, status):
    timestamp = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} | {method} | {path} | HTTP {status}\n")


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ok","service":"log-lab"}'
            status = 200
        else:
            body = b'{"error":"not_found"}'
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

        write_log("GET", self.path, status)


server = HTTPServer(("127.0.0.1", 9096), Handler)

print("Cyber Lab Log Lab running on 127.0.0.1:9096")
server.serve_forever()
