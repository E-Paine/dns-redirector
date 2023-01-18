import dns_component
import http_component
import https_component
import util

if __name__ == "__main__":
    util.set_config_file("config.json")

    dns = dns_component.get_server()
    http = http_component.get_server()
    https = https_component.get_server()
    dns.start()
    http.start()
    https.start()

    try:
        dns.join()
    except KeyboardInterrupt:
        pass
    finally:
        dns.shutdown()
        http.shutdown()
        https.shutdown()
    dns.join()
    http.join()
    https.join()
