import ssl

import http_component


def get_server():
    component = http_component.get_server("https_port")
    component.server.socket = ssl.wrap_socket(
        component.server.socket,
        server_side=True,
        certfile="cert.pem",
        keyfile="key.pem",
        ssl_version=ssl.PROTOCOL_TLS,
    )
    return component
