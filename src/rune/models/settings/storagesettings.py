from abc import ABC, abstractmethod
from typing import Dict, Self
from dataclasses import dataclass
import os

from platformdirs import PlatformDirs

class StorageSettings(ABC):
    FILE_BASED: str = "local"

    @property
    def mode(self) -> str: raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> Dict: raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict | None) -> "StorageSettings":
        if not d: return cls.default()
        match d["mode"]:
            case cls.FILE_BASED:
                return FileBasedStorageSettings.from_dict(d)
            case _:
                raise ValueError()

    @classmethod
    def default(cls) -> "StorageSettings":
        return FileBasedStorageSettings.default()

@dataclass
class FileBasedStorageSettings(StorageSettings):
    file: str

    @property
    def mode(self) -> str: return StorageSettings.FILE_BASED

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode,
            "file": self.file
        }
    
    @classmethod
    def from_dict(cls, d: Dict | None) -> Self:
        if not d: return cls.default()
        return cls(d["file"])

    @classmethod
    def default(cls) -> Self:
        dirs = PlatformDirs("rune", None)
        return cls(
            file = os.path.join(dirs.user_config_dir, "secrets.json")
        )



