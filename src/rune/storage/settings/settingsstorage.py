import json
from rune.models.settings.settings import Settings

from platformdirs import PlatformDirs
import os


class SettingsStorageManager:
    dirs = PlatformDirs("rune", None)
    config_dir = dirs.user_config_dir
    settings_file = os.path.join(config_dir, "settings.json")

    def __init__(self) -> None:
        self._ensure_settings()

    def _ensure_settings(self) -> None:
        if not os.path.exists(self.settings_file):
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.settings_file, "w") as f:
                json.dump(Settings.default().to_dict(), f, indent=4)

    def load_settings(self) -> Settings:
        with open(self.settings_file, "r") as f:
            d = json.load(f)
            return Settings.from_dict(d)

    
    def save_settings(self, settings: Settings) -> None:
        with open(self.settings_file, "w") as f:
            json.dump(settings.to_dict(), f, indent=4)


