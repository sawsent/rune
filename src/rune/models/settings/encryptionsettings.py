from abc import ABC, abstractmethod
from typing import Dict, Self
from dataclasses import dataclass

class EncryptionSettings(ABC):
    AES_GCM: str = "aesgcm"

    @property
    def mode(self) -> str: raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> Dict: raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict | None) -> "EncryptionSettings":
        if not d: return cls.default()
        match d["mode"]:
            case cls.AES_GCM:
                return AES_GCMEncryptionSettings.from_dict(d)
            case _:
                raise ValueError(f"Unknown encryption mode '{d["mode"]}'")

    @classmethod
    def from_mode(cls, mode: str) -> "EncryptionSettings":
        match mode:
            case cls.AES_GCM:
                return AES_GCMEncryptionSettings.default()
            case _:
                raise ValueError(f"Unknown encryption mode '{mode}'")

    @classmethod
    def default(cls) -> "EncryptionSettings":
        return AES_GCMEncryptionSettings.default()



@dataclass
class AES_GCMEncryptionSettings(EncryptionSettings):
    @property
    def mode(self) -> str: return "aesgcm"

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode,
        }
    
    @classmethod
    def from_dict(cls, d: Dict | None) -> Self:
        if not d: return cls.default()
        return cls()

    @classmethod
    def default(cls) -> Self:
        return cls()


