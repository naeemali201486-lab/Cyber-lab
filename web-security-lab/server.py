from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from html import escape
from rate_limit import allowed


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        log_dir = Path.home() / "cyber-lab" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "web-security-lab.log"

        message = "%s - - [%s] %s\\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        )

        with log_file.open(
            "a",
            encoding="utf-8"
        ) as f:
            f.write(message)

    def send_security_headers(self):
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'"
        )
        self.send_header(
            "X-Content-Type-Options",
            "nosniff"
        )
        self.send_header(
            "Referrer-Policy",
            "no-referrer"
        )

    def do_GET(self):
        path = urlparse(self.path)

        if path.path == "/":

            body = """
<!doctype html>
<html>
<head>
<title>Web Security Lab</title>
</head>
<body>

<h1>Web Security Lab</h1>
<p>Local practice environment</p>

<form action="/search" method="get">
    <input name="q" placeholder="Search">
    <button type="submit">Search</button>
</form>

<p><a href="/health">Health check</a></p>

</body>
</html>
"""

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body.encode())

        elif path.path == "/health":

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(b"OK")

        elif path.path == "/search":

            # Rate limiting
            if not allowed():
                self.send_response(429)
                self.send_header(
                    "Content-Type",
                    "text/plain"
                )
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(
                    b"Too Many Requests"
                )
                return

            query = parse_qs(
                path.query
            ).get("q", [""])[0]

            # HTML escaping
            safe_query = escape(query)

            body = f"""
<!doctype html>
<html>
<body>

<h1>Search</h1>
<p>You searched for: {safe_query}</p>

</body>
</html>
"""

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html"
            )
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body.encode())

        else:

            self.send_response(404)
            self.send_security_headers()
            self.end_headers()


server = HTTPServer(
    ("127.0.0.1", 9098),
    Handler
)

print(
    "Web Security Lab running on "
    "127.0.0.1:9098"
)

server.serve_forever()
