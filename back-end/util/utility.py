import json
import os


def load_from_config(config_path: str, to_fetch: str):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config[to_fetch]
    else:
        return "404"
