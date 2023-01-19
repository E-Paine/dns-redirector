import datetime
import json
import threading
import time
from typing import Any, Dict, Optional
from urllib import parse

from dns import resolver


config: Optional[Dict[str, Any]] = None
excluded = []


def get_config():
    return config


def set_config(new_conf):
    global config
    for device in excluded:
        del new_conf["device_specific"][device]
    for device in new_conf["device_specific"].values():
        device["allowed_domains"] = set(
            device["allowed_domains"]
            + [parse.urlparse(device["redirect"]).netloc.split(":")[0]]
        )
    new_conf["activation_time"] = datetime.datetime.strptime(
        new_conf["activation_time"], "%Y-%m-%d %H:%M:%S"
    )
    config = new_conf
    resolver.get_default_resolver().nameservers = [new_conf["dns_upstream"]]


def set_config_file(file):
    with open(file) as f:
        set_config(json.load(f))
    threading.Thread(target=_set_conf_loop, args=(file,), daemon=True).start()


def exclude_device(device):
    excluded.append(device)
    del config["device_specific"][device]


def _set_conf_loop(file):
    while True:
        time.sleep(get_config()["config_refresh_time"])
        try:
            with open(file) as f:
                set_config(json.load(f))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(e)
