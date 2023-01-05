import http.server
import threading

from util import get_config


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        config = get_config()
        device = config["device_specific"].get(self.client_address[0])
        if device is None:
            return
        self.send_response(302)
        self.send_header("Location", device["redirect"])
        self.end_headers()


def get_server():
    server = http.server.HTTPServer(
        ("0.0.0.0", get_config()["http_port"]), HTTPRequestHandler
    )
    thread = threading.Thread(target=server.serve_forever)
    return server, thread
