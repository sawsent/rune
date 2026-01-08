from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Dict, ClassVar, Type, Self


class SessionCmd(ABC):
    START_SESSION: ClassVar[str] = "start"
    END_SESSION: ClassVar[str] = "end"
    GET_SESSION_KEY: ClassVar[str] = "get"
    SESSION_STATUS: ClassVar[str] = "status"
    HANDSHAKE: ClassVar[str] = "handshake"

    _registry: ClassVar[Dict[str, Type["SessionCmd"]]] = {}

    CMD: ClassVar[str]

    def to_dict(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, d: Dict) -> "SessionCmd":
        try:
            cmd = d["type"]
        except:
            raise ValueError(f"Got unexpected command type: {d.get("type")}") from None

        match cmd:
            case cls.START_SESSION: return StartSessionCmd.from_dict(d)
            case cls.END_SESSION: return EndSessionCmd.from_dict(d)
            case cls.GET_SESSION_KEY: return GetSessionKeyCmd.from_dict(d)
            case cls.SESSION_STATUS: return SessionStatusCmd.from_dict(d)
            case cls.HANDSHAKE: return HandshakeCmd.from_dict(d)

        raise ValueError(f"Got unexpected command type: {d.get("type")}") from None

@dataclass
class StartSessionCmd(SessionCmd):
    CMD: ClassVar[str] = SessionCmd.START_SESSION

    session_key: str
    ttl: int
    user: str

    def to_dict(self) -> Dict:
        return {
            "type": self.CMD,
            "session_key": self.session_key,
            "ttl": self.ttl,
            "user": self.user
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["session_key"], d["ttl"], d["user"])


@dataclass
class EndSessionCmd(SessionCmd):
    CMD: ClassVar[str] = SessionCmd.END_SESSION

    def to_dict(self) -> Dict:
        return {
            "type": self.CMD,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls()


@dataclass
class GetSessionKeyCmd(SessionCmd):
    CMD: ClassVar[str] = SessionCmd.GET_SESSION_KEY

    user: str

    def to_dict(self) -> Dict:
        return {
            "type": self.CMD,
            "user": self.user
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["user"])


@dataclass
class SessionStatusCmd(SessionCmd):
    CMD: ClassVar[str] = SessionCmd.SESSION_STATUS

    def to_dict(self) -> Dict:
        return {"type": self.CMD}

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls()

@dataclass
class HandshakeCmd(SessionCmd):
    CMD: ClassVar[str] = SessionCmd.HANDSHAKE

    def to_dict(self) -> Dict:
        return {"type": self.CMD}

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls()

