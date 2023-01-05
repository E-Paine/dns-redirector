import json

import dns_component
import util

with open("config.json") as f:
    config = json.load(f)

util.set_config(config)
dns_server, dns_thread = dns_component.get_server()
dns_thread.start()
try:
    dns_thread.join()
except KeyboardInterrupt:
    pass
finally:
    dns_server.shutdown()
dns_thread.join()
