import json
from typing import Dict, Optional
from rune.models.settings.settings import Settings

from platformdirs import PlatformDirs
import os
from pathlib import Path


class SettingsStorageManager:

    def __init__(self, config_dir: Path | None = None, settings_file: Path | None = None, profiles_file: Path | None = None) -> None:
        self.config_dir: Path = config_dir or Path(PlatformDirs("rune", None).user_config_dir)
        self.settings_file: Path = settings_file or Path(os.path.join(self.config_dir, "settings.json"))
        self.profiles_file: Path = profiles_file or Path(os.path.join(self.config_dir, "profiles.json"))
        self._ensure_settings()

    def _ensure_settings(self) -> None:
        if not self.settings_file.exists():
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, "x") as f:
                json.dump(Settings.default().to_dict(), f, indent=4)

    def _ensure_profiles(self) -> None:
        if not self.profiles_file.exists():
            self.profiles_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.profiles_file, "x") as f:
                json.dump({}, f, indent=4)

    def load_settings(self) -> Settings:
        with open(self.settings_file, "r") as f:
            d = json.load(f)
            return Settings.from_dict(d)
    
    def save_settings(self, settings: Settings) -> None:
        with open(self.settings_file, "w") as f:
            json.dump(settings.to_dict(), f, indent=4)

    def get_profiles(self) -> Dict[str, Settings]:
        self._ensure_profiles()
        with open(self.profiles_file, "r") as f:
            profile_d = json.load(f)
            return {name: Settings.from_dict(settings) for name, settings in profile_d.items()}

    def get_profile(self, name: str) -> Optional[Settings]:
        profiles = self.get_profiles()
        profile: Settings | None = profiles.get(name)
        return profile if profile else None

    def delete_profile(self, name: str) -> None:
        profiles = self.get_profiles()
        removed = {k: v for k, v in profiles.items() if not name == k}
        self._store_profiles(removed)

    def save_profile(self, settings: Settings, name: str) -> None:
        profiles = self.get_profiles()
        profiles[name] = settings
        self._store_profiles(profiles)

    def _store_profiles(self, profiles: Dict[str, Settings]) -> None:
        self._ensure_profiles()
        with open(self.profiles_file, "w") as f:
            profile_dict = {name: profile.to_dict() for name, profile in profiles.items()}
            json.dump(profile_dict, f, indent=4)





