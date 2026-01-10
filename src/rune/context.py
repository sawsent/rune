from typing import Self
from rune.crypto.base import Encrypter
from rune.crypto.factory import get_encrypter
from rune.models.settings.settings import Settings
from rune.session.base import SessionManager
from rune.session.factory import get_session_manager
from rune.storage.secrets.base import StorageManager
from rune.storage.secrets.factory import get_storage_manager
from rune.storage.settings.settingsstorage import SettingsStorageManager

class Context:
    _context: Self | None = None

    def __init__(
        self,
        settings_manager: SettingsStorageManager | None,
        encrypter: Encrypter | None,
        storage_manager: StorageManager | None,
        session_manager: SessionManager | None

    ) -> None:
        self.settings_manager: SettingsStorageManager = settings_manager or SettingsStorageManager()
        self.settings: Settings = self.settings_manager.load_settings()
        self.configured_encrypter: Encrypter = encrypter or get_encrypter(self.settings)
        self.storage_manager: StorageManager = storage_manager or get_storage_manager(self.settings)
        self.session_manager: SessionManager = session_manager or get_session_manager(self.settings)

    def save_settings(self, force: bool = False) -> None:
        """
        Saves the settings if they are marked as dirty (or force).
        Dirty settings means something changed.
        """
        if self.settings._dirty or force:
            self.settings_manager.save_settings(self.settings)

    @classmethod
    def get(cls) -> Self:
        if cls._context is not None:
            return cls._context
        raise RuntimeError("Context is not set. Call `Context.build()` first.")

    @classmethod
    def build(
        cls,
        settings_manager: SettingsStorageManager | None = None,
        encrypter: Encrypter | None = None,
        storage_manager: StorageManager | None = None,
        session_manager: SessionManager | None = None,
    ) -> Self:
        if not cls._context:
            cls._context = cls(settings_manager, encrypter, storage_manager, session_manager)
            return cls._context
        raise RuntimeError("Context is already built")

    @classmethod
    def update(
        cls,
        settings_manager: SettingsStorageManager | None = None,
        encrypter: Encrypter | None = None,
        storage_manager: StorageManager | None = None,
        session_manager: SessionManager | None = None,
    ) -> Self:
        if cls._context:
            cls._context = cls(settings_manager, encrypter, storage_manager, session_manager)
            return cls._context
        raise RuntimeError("Context is not set. Call `Context.build()` first.")


    @classmethod
    def reset(cls) -> None:
        cls._context = None


