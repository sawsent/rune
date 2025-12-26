from __future__ import annotations

from abc import ABC
from typing import Dict, ClassVar, Self


class SessionResp(ABC):
    STATUS: ClassVar[str] = "status"
    GET_KEY: ClassVar[str] = "get_key"
    SUCCESS: ClassVar[str] = "success"
    FAILURE: ClassVar[str] = "failure"
    HANDSHAKE: ClassVar[str] = "handshake"

    RESP: ClassVar[str]

    def to_dict(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, d: Dict) -> "SessionResp":
        try:
            resp_type = d["type"]
        except:
            raise ValueError(f"Got unexpected response type: {d.get("type")}") from None

        match resp_type:
            case cls.STATUS: return StatusResponse.from_dict(d)
            case cls.GET_KEY: return GetKeyResponse.from_dict(d)
            case cls.SUCCESS: return SuccessResponse.from_dict(d)
            case cls.FAILURE: return FailureResponse.from_dict(d)
            case cls.HANDSHAKE: return HandshakeResp.from_dict(d)

        raise ValueError(f"Got unexpected response type: {d.get("type")}") from None

class StatusResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.STATUS

    def __init__(self, remaining_ttl: int, user: str) -> None:
        self.remaining_ttl = remaining_ttl
        self.user = user

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "ttl": self.remaining_ttl,
            "u": self.user,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(
            remaining_ttl=d["ttl"],
            user=d["u"],
        )


class GetKeyResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.GET_KEY

    def __init__(self, session_key: str) -> None:
        self.session_key = session_key

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "sk": self.session_key,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["sk"])


class SuccessResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.SUCCESS

    def __init__(self, message: str) -> None:
        self.message = message

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "msg": self.message,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["msg"])


class FailureResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.FAILURE

    def __init__(self, message: str) -> None:
        self.message = message

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "msg": self.message,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["msg"])

class HandshakeResp(SessionResp):
    RESP: ClassVar[str] = SessionResp.HANDSHAKE

    def __init__(self, all_good: bool) -> None:
        self.all_good = all_good

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "g": self.all_good
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["g"])

