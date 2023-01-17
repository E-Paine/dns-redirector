import json
import threading
import time
from urllib import parse


config = None


def get_config():
    return config


def set_config(new_conf):
    global config
    for device in new_conf["device_specific"].values():
        device["allowed_domains"] = set(
            device["allowed_domains"]
            + [parse.urlparse(device["redirect"]).netloc.split(":")[0]]
        )
    config = new_conf


def set_config_file(file):
    with open(file) as f:
        set_config(json.load(f))
    threading.Thread(target=_set_conf_loop, args=(file,), daemon=True).start()


def _set_conf_loop(file):
    while True:
        time.sleep(get_config()["config_refresh_time"])
        try:
            with open(file) as f:
                set_config(json.load(f))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(e)
