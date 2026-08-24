from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path)

        if path.path == "/":
            body = """
<h1>Cyber Lab Hacking Practice</h1>
<p>Local training server.</p>
<ul>
<li><a href="/login">Login Lab</a></li>
<li><a href="/search?q=test">Search Lab</a></li>
</ul>
"""
        elif path.path == "/login":
            body = """
<h2>Login Lab</h2>
<form>
<input name="username" placeholder="Username">
<input name="password" type="password" placeholder="Password">
<button>Login</button>
</form>
"""
        elif path.path == "/search":
            query = parse_qs(path.query).get("q", [""])[0]
            body = f"<h2>Search Lab</h2><p>Search: {query}</p>"
        else:
            self.send_error(404)
            return

        data = body.encode()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

server = HTTPServer(("127.0.0.1", 9093), LabHandler)

print("Hacking Practice Lab running on http://127.0.0.1:9093")
server.serve_forever()
