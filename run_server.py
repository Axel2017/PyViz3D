# Use to create local host
import http.server
import socketserver
import sys

if __name__ == "__main__":
    PORT = int(sys.argv[1])

    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({".js": "application/javascript"})

    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("Started server on port " + str(PORT))
    httpd.serve_forever()
