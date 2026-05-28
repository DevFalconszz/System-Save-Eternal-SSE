import json
import os
from typing import Any, Dict, Optional

CONFIG_DIR = os.path.expanduser("~/.config/sse")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "save_repo_path": "",
    "github": {
        "token": "",
        "repo_url": "",
        "remote_name": "origin"
    },
    "google_drive": {
        "client_id": "",
        "client_secret": "",
        "folder_id": ""
    },
    "telegram": {
        "api_id": 0,
        "api_hash": "",
        "phone": "",
        "chat_id": ""
    }
}


def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config() -> Dict[str, Any]:
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return dict(DEFAULT_CONFIG)


def save_config(config: Dict[str, Any]):
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get(key: str, default: Any = None) -> Any:
    config = load_config()
    parts = key.split(".")
    val = config
    for part in parts:
        if isinstance(val, dict):
            val = val.get(part, {})
        else:
            return default
    return val if val != {} else default


def set_key(key: str, value: Any):
    config = load_config()
    parts = key.split(".")
    target = config
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value
    save_config(config)
