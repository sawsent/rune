from abc import ABC, abstractmethod
from typing import Dict, Self
from dataclasses import dataclass

class EncryptionSettings(ABC):
    AES_GCM: str = "aesgcm"

    @abstractmethod
    def mode(self) -> str: raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> Dict: raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict) -> "EncryptionSettings":
        match d["mode"]:
            case cls.AES_GCM:
                return AES_GCMEncryptionSettings.from_dict(d)
            case _:
                raise ValueError()

    @classmethod
    def default(cls) -> "EncryptionSettings":
        return AES_GCMEncryptionSettings.default()



@dataclass
class AES_GCMEncryptionSettings(EncryptionSettings):
    def mode(self) -> str: return "aesgcm"

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode(),
        }
    
    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls()

    @classmethod
    def default(cls) -> Self:
        return cls()


