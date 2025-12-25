from __future__ import annotations

from abc import ABC
from typing import Dict, ClassVar, Type, Self


class SessionResp(ABC):
    STATUS: ClassVar[str] = "status"
    GET_KEY: ClassVar[str] = "get_key"
    SUCCESS: ClassVar[str] = "success"
    FAILURE: ClassVar[str] = "failure"

    _registry: ClassVar[Dict[str, Type["SessionResp"]]] = {}

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

        raise ValueError(f"Got unexpected response type: {d.get("type")}") from None

class StatusResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.STATUS

    def __init__(self, remaining_ttl: int, user: str) -> None:
        self.remaining_ttl = remaining_ttl
        self.user = user

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "remaining_ttl": self.remaining_ttl,
            "user": self.user,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(
            remaining_ttl=d["remaining_ttl"],
            user=d["user"],
        )


class GetKeyResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.GET_KEY

    def __init__(self, session_key: str) -> None:
        self.session_key = session_key

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "session_key": self.session_key,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["session_key"])


class SuccessResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.SUCCESS

    def __init__(self, message: str) -> None:
        self.message = message

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["message"])


class FailureResponse(SessionResp):
    RESP: ClassVar[str] = SessionResp.FAILURE

    def __init__(self, message: str) -> None:
        self.message = message

    def to_dict(self) -> Dict:
        return {
            "type": self.RESP,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(d["message"])

