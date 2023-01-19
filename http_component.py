import http.server
import threading

from base_component import Component
from util import get_config, exclude_device


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        config = get_config()
        device = config["device_specific"].get(self.client_address[0])
        self.send_header("Content-type", "text/html; charset=utf-8")

        if device is None:
            self.send_response(404)
            self.end_headers()
            return

        if self.path == "/disable_device":
            exclude_device(self.client_address[0])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                "DNS redirection has now been disabled for your device. "
                f"It may take up to {get_config()['dns_ttl']} second/s for this "
                "to take effect.".encode("utf-8")
            )
            return

        self.send_response(302)
        self.send_header("Location", device["redirect"])
        self.end_headers()


def get_server(key="http_port"):
    server = http.server.HTTPServer(("0.0.0.0", get_config()[key]), HTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    return Component(server, thread)
