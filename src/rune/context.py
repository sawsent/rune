from typing import Self
from rune.encryption.base import Encrypter
from rune.models.settings.settings import Settings
from rune.storage.secrets.base import StorageManager
from rune.storage.secrets.factory import get_storage_manager
from rune.storage.settings.settingsstorage import SettingsStorageManager
from rune.encryption.factory import get_encrypter

class Context:
    _context: Self | None = None

    def __init__(self) -> None:
        self.settings_manager: SettingsStorageManager = SettingsStorageManager()
        self.settings: Settings = self.settings_manager.load_settings()
        self.configured_encrypter: Encrypter = get_encrypter(self.settings)
        self.storage_manager: StorageManager = get_storage_manager(self.settings)

    @classmethod
    def get(cls) -> Self:
        if cls._context is not None:
            return cls._context
        raise RuntimeError("Context is not set. Call `Context.build()` first.")

    @classmethod
    def build(cls) -> Self:
        if not cls._context:
            cls._context = cls()
            return cls._context
        raise RuntimeError("Context is already built")

    @classmethod
    def update(cls) -> Self:
        cls._context = cls()
        return cls._context

    @classmethod
    def reset(cls) -> None:
        cls._context = None


