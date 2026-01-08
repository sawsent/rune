from dataclasses import dataclass, field
from typing import Optional, Dict, Self

@dataclass
class SecretField:
    ciphertext: str
    nonce: Optional[str] = None
    tag: Optional[str] = None
    salt: Optional[str] = None
    algorithm: Optional[str] = None
    deleted: bool = False
    params: Dict[str, str] = field(default_factory=dict)

    version: int = 1

    def soft_delete(self) -> Self:
        self.deleted = True
        return self

    def restore(self) -> Self:
        self.deleted = False
        return self

    def to_dict(self) -> Dict:
        return {
            "ciphertext": self.ciphertext,
            "nonce": self.nonce,
            "tag": self.tag,
            "salt": self.salt,
            "algorithm": self.algorithm,
            "deleted": self.deleted,
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
            deleted=data.get("deleted", False),
            params=data.get("params", {}),
            version=data.get("version", 1)
        )


