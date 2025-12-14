from abc import ABC, abstractmethod
from typing import Dict, Self
from dataclasses import dataclass

class StorageSettings(ABC):
    FILE_BASED: str = "local"

    @abstractmethod
    def mode(self) -> str: raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> Dict: raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict) -> "StorageSettings":
        match d["mode"]:
            case cls.FILE_BASED:
                return FileBasedStorageSettings.from_dict(d)
            case _:
                raise ValueError()

@dataclass
class FileBasedStorageSettings(StorageSettings):
    file: str

    def mode(self) -> str: return StorageSettings.FILE_BASED

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode(),
            "file": self.file
        }
    
    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["file"])



