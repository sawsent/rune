from typing import Self, Dict


class Secret:
    def __init__(self, name: str, ciphertext: str, timestamp: int = 0) -> None:
        self.name = name
        self.ciphertext = ciphertext
        self.timestamp = timestamp

    @classmethod
    def from_dict(cls, name: str, d: Dict) -> Self:
        return cls(name, d["ciphertext"])
