from dataclasses import dataclass
from typing import Self


@dataclass
class SessionStatus:
    started: bool
    ttl: int | None
    user: str | None

    @classmethod
    def NOT_STARTED(cls) -> Self:
        return cls(False, None, None)

    @classmethod
    def STARTED_UNKNOWN(cls) -> Self:
        return cls(True, None, None)
