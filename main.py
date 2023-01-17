import json

import dns_component
import http_component
import util

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    util.set_config(config)
    dns = dns_component.get_server()
    http = http_component.get_server(80)
    dns.start()
    http.start()
    try:
        dns.join()
    except KeyboardInterrupt:
        pass
    finally:
        dns.shutdown()
        http.shutdown()
    dns.join()
    http.join()
