from dataclasses import dataclass, field
from typing import List, Self

@dataclass
class Namespace:
    ns: List[str] = field(default_factory=list)

    @property
    def to_string(self):
        return "/".join(self.ns).removeprefix("/").removesuffix("/").strip()

    @classmethod
    def from_string(cls, s: str | None) -> Self:
        if not s:
            return cls()
        else:
            parts = s.split("/")
            return cls(parts)

