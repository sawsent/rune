from typing import Dict, Optional
from platformdirs import PlatformDirs
import os
import json

from rune.models.result import Result, Success

def default_settings(config_path) -> Dict: 
    return {
        "encryption": "aesgcm",
        "storage": {
            "mode": "local",
            "file": os.path.join(config_path, "secrets.json")
        }
    }

def update_settings(encryption: Optional[str] = None,
                    storage_mode: Optional[str] = None,
                    storage_file: Optional[str] = None) -> Result[str]:
    d = get_settings_dict()
    if encryption is not None:
        d["encryption"] = encryption
    if storage_mode is not None:
        d["storage"]["mode"] = storage_mode
    if storage_file is not None:
        d["storage"]["file"] = storage_file

    settings_path = get_settings_path()
    with open(settings_path, "w") as f:
        json.dump(d, f, indent=4)

    return Success(f"Updated settings at '{settings_path}'")


def get_config_dir() -> str:
    dirs = PlatformDirs("rune", None)
    return dirs.user_config_dir

def get_settings_path() -> str:
    config_dir = get_config_dir()
    settings_file = os.path.join(config_dir, "settings.json")
    return settings_file

def ensure_settings_exist() -> str:
    dirs = PlatformDirs("rune", None)
    config_dir = dirs.user_config_dir

    os.makedirs(config_dir, exist_ok=True)

    settings_file = get_settings_path()

    if not os.path.exists(settings_file):
        with open(settings_file, "w") as f:
            json.dump(default_settings(config_dir), f, indent=4)

    return settings_file

def ensure_secrets_exist() -> str:
    secrets_path = get_secrets_path()
    if not os.path.exists(secrets_path) or os.path.getsize(secrets_path) == 0:
        with open(secrets_path, "w") as f:
            json.dump({}, f, indent=4)
    return secrets_path

def get_settings_dict() -> Dict:
    try:
        with open(get_settings_path(), "r") as f:
            return json.load(f)
    except:
        return default_settings(get_config_dir())

def get_secrets_path() -> str:
    settings = get_settings_dict()
    return settings["storage"]["file"]

def get_configured_encryption_identifier() -> str:
    settings = get_settings_dict()
    return settings["encryption"]

def get_configured_storage_manager_identifier() -> str:
    settings = get_settings_dict()
    return settings["storage"]["mode"]
