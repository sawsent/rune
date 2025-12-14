from dataclasses import dataclass
from typing import Dict, Self

from rune.models.settings.encryptionsettings import EncryptionSettings
from rune.models.settings.storagesettings import StorageSettings


@dataclass
class Settings:
    encryption: EncryptionSettings
    storage: StorageSettings

    def to_dict(self) -> Dict:
        return {
            "encryption": self.encryption.to_dict(),
            "storage": self.storage.to_dict()
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(
            encryption = EncryptionSettings.from_dict(d["encryption"]),
            storage = StorageSettings.from_dict(d["storage"])
        )

    @classmethod
    def default(cls) -> Self:
        return cls(
            encryption = EncryptionSettings.default(),
            storage = StorageSettings.default(),
        )


