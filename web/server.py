from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(("127.0.0.1", 8080), SimpleHTTPRequestHandler)

print("Cyber Lab Web running on http://127.0.0.1:8080")
server.serve_forever()
