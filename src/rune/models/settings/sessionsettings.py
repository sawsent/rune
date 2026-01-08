from abc import ABC, abstractmethod
from typing import Dict, Self
from dataclasses import dataclass

class SessionSettings(ABC):
    DAEMON: str = "daemon"

    @property
    def mode(self) -> str: raise NotImplementedError()

    @property
    def default_ttl(self) -> int: raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> Dict: raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict | None) -> "SessionSettings":
        if not d: return cls.default()
        match d["mode"]:
            case cls.DAEMON:
                return DaemonSessionSettings.from_dict(d)
            case _:
                raise ValueError(f"Unknown encryption mode '{d["mode"]}'")

    @classmethod
    def from_mode(cls, mode: str) -> "SessionSettings":
        match mode:
            case cls.DAEMON:
                return DaemonSessionSettings.default()
            case _:
                raise ValueError(f"Unknown encryption mode '{mode}'")

    @classmethod
    def default(cls) -> "SessionSettings":
        return DaemonSessionSettings.default()



@dataclass
class DaemonSessionSettings(SessionSettings):
    port: int
    _default_ttl: int

    @property
    def mode(self) -> str: return SessionSettings.DAEMON

    @property
    def default_ttl(self) -> int: return self._default_ttl

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode,
            "port": self.port,
            "default_ttl": self.default_ttl,
        }
    
    @classmethod
    def from_dict(cls, d: Dict | None) -> Self:
        if not d: return cls.default()
        return cls(
            port=d.get("port", cls.default().port),
            _default_ttl = d.get("default_ttl", cls.default().default_ttl)
        )

    @classmethod
    def default(cls) -> Self:
        return cls(
            port=5000,
            _default_ttl=300
        )


