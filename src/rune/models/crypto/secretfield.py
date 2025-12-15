from dataclasses import dataclass, field
from typing import Optional, Dict, Self

@dataclass
class SecretField:
    ciphertext: str
    nonce: Optional[str] = None
    tag: Optional[str] = None
    salt: Optional[str] = None
    algorithm: Optional[str] = None
    params: Dict[str, str] = field(default_factory=dict)

    version: int = 1

    def to_dict(self) -> Dict:
        return {
            "ciphertext": self.ciphertext,
            "nonce": self.nonce,
            "tag": self.tag,
            "salt": self.salt,
            "algorithm": self.algorithm,
            "params": self.params,
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(
            ciphertext=data["ciphertext"],
            nonce=data.get("nonce"),
            tag=data.get("tag"),
            salt=data.get("salt"),
            algorithm=data.get("algorithm"),
            params=data.get("params", {}),
            version=data.get("version", 1)
        )


