import json

import dns_component
import http_component
import util

with open("config.json") as f:
    config = json.load(f)

util.set_config(config)
dns_server, dns_thread = dns_component.get_server()
http_server, http_thread = http_component.get_server()
dns_thread.start()
http_thread.start()
try:
    dns_thread.join()
    http_thread.join()
except KeyboardInterrupt:
    pass
finally:
    dns_server.shutdown()
    http_server.shutdown()
dns_thread.join()
http_thread.join()
