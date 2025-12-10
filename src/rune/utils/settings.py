from typing import Dict
from platformdirs import PlatformDirs
import os
import json

def default_settings(config_path) -> Dict[str, str]: 
    return {
        "secrets_file": os.path.join(config_path, "secrets.json"),
        "encryption": "no-encryption",
        "storage": "local"
    }

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

    if not os.path.exists(settings_file) or True:
        with open(settings_file, "w") as f:
            json.dump(default_settings(config_dir), f, indent=4)

    return settings_file

def get_settings_dict() -> Dict[str, str]:
    try:
        with open(get_settings_path(), "r") as f:
            return json.load(f)
    except:
        return default_settings(get_config_dir())

def get_secrets_path() -> str:
    settings = get_settings_dict()
    return settings["secrets_file"]

def get_configured_encryption_identifier() -> str:
    settings = get_settings_dict()
    return settings["encryption"]

def get_configured_storage_manager_identifier() -> str:
    settings = get_settings_dict()
    return settings["storage"]
