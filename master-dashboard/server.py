from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
import json

SERVICES = {
    "service-test": "http://127.0.0.1:9094/health",
    "dashboard": "http://127.0.0.1:9095/api/status",
    "log-lab": "http://127.0.0.1:9096/health",
}

class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/status":
            result = {}

            for name, url in SERVICES.items():
                try:
                    with urlopen(url, timeout=2) as response:
                        result[name] = {
                            "status": "online",
                            "http": response.status
                        }
                except Exception:
                    result[name] = {
                        "status": "offline"
                    }

            body = json.dumps(result).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()

server = HTTPServer(("127.0.0.1", 9097), Handler)

print("Cyber Lab Master Dashboard running on 127.0.0.1:9097")
server.serve_forever()
