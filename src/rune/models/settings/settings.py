from dataclasses import dataclass
from typing import Dict, Optional, Self

from rune.models.settings.encryptionsettings import EncryptionSettings
from rune.models.settings.sessionsettings import SessionSettings
from rune.models.settings.storagesettings import StorageSettings


@dataclass
class Settings:
    encryption: EncryptionSettings
    storage: StorageSettings
    session: SessionSettings
    active_user: Optional[str]

    _dirty: bool = False

    def to_dict(self) -> Dict:
        ret: Dict = {
            "encryption": self.encryption.to_dict(),
            "storage": self.storage.to_dict(),
            "session": self.session.to_dict(),
        }
        if self.active_user:
            ret["active_user"] = self.active_user
        return ret

    def update(self,
               encryption: EncryptionSettings | None = None,
               storage: StorageSettings | None = None,
               session: SessionSettings | None = None,
               active_user: str | None = None) -> None:
        self.encryption = encryption or self.encryption
        self.storage = storage or self.storage
        self.session = session or self.session
        self.active_user = active_user or self.active_user
        self._dirty = True

    def reset(self,
              encryption: bool = False,
              storage: bool = False,
              session: bool = False,
              active_user: bool = False) -> None:
        self._dirty = True
        default = self.default()
        if encryption:  self.encryption = default.encryption
        if storage:     self.storage = default.storage
        if session:     self.session = default.session
        if active_user: self.active_user = default.active_user

    def dirty(self) -> Self:
        self._dirty = True
        return self

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(
            encryption = EncryptionSettings.from_dict(d.get("encryption")),
            storage = StorageSettings.from_dict(d.get("storage")),
            session= SessionSettings.from_dict(d.get("session")),
            active_user = d.get("active_user", None)
        )

    @classmethod
    def default(cls) -> Self:
        return cls(
            encryption = EncryptionSettings.default(),
            storage = StorageSettings.default(),
            session = SessionSettings.default(),
            active_user = None,
        )


