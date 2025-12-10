from typing import Self, Dict


class Secret:
    def __init__(self, name: str, data: Dict, timestamp: int = 0) -> None:
        self.name = name
        self.data = data
        self.timestamp = timestamp

    @classmethod
    def from_dict(cls, name: str, d: Dict) -> Self:
        return cls(name, d["data"])
