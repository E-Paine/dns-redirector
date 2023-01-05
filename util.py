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
