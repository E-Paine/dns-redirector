import socket
import socketserver
import threading

import dnslib
from dns import exception, resolver

from base_component import Component
from util import get_config


resolver.get_default_resolver().nameservers = ["8.8.8.8"]


def get_local_addr():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("8.8.8.8", 80))
        addr = sock.getsockname()[0]
    return "AAAA" if ":" in addr else "A", addr


def handle_request(data, source):
    config = get_config()
    try:
        request = dnslib.DNSRecord.parse(data)
    except dnslib.DNSError as e:
        print(e)
        return b""
    qname = str(request.q.qname)
    qtype_e = request.q.qtype
    qtype = dnslib.QTYPE[qtype_e]

    reply = dnslib.DNSRecord(
        dnslib.DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q
    )
    device = config["device_specific"].get(source)
    if device is None:
        forward_request(reply, qname, qtype, qtype_e, config)
        return reply.pack()

    if qname[:-1] in device["allowed_domains"]:
        forward_request(reply, qname, qtype, qtype_e, config)
    elif qtype == FORWARD[0]:
        reply.add_answer(
            dnslib.RR(
                rname=qname,
                rtype=qtype_e,
                rclass=1,
                ttl=config["dns_ttl"],
                rdata=getattr(dnslib, qtype)(FORWARD[1]),
            )
        )
    return reply.pack()


def forward_request(reply, qname, qtype, qtype_e, config):
    try:
        for ans in resolver.resolve(qname, qtype):
            reply.add_answer(
                dnslib.RR(
                    rname=qname,
                    rtype=qtype_e,
                    rclass=1,
                    ttl=config["dns_ttl"],
                    rdata=getattr(dnslib, qtype)(ans.to_text()),
                )
            )
    except exception.DNSException as e:
        print(e)


def get_server():
    server = socketserver.ThreadingUDPServer(
        ("0.0.0.0", get_config()["dns_port"]), DNSRequestHandler
    )
    thread = threading.Thread(target=server.serve_forever)
    return Component(server, thread)


class DNSRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request[1].sendto(
            handle_request(self.request[0], self.client_address[0]),
            self.client_address,
        )


FORWARD = get_local_addr()
