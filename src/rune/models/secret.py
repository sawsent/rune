from typing import Self, Dict, Optional, List
from dataclasses import dataclass, field
import uuid
from datetime import datetime

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

@dataclass
class Secret:
    name: str
    algorithm: str
    namespace: str = ""
    fields: Dict[str, SecretField] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    version: int = 1

    def update(self,
               name: str | None = None,
               algorithm: str | None = None,
               namespace: str | None = None,
               fields: Dict[str, SecretField] | None = None,
               tags: List[str] | None = None,
               metadata: Dict[str, str] | None = None,
               version: int | None = None) -> Self:
        return type(self)(
            name = name or self.name,
            algorithm = algorithm or self.algorithm,
            namespace = namespace or self.namespace,
            fields = fields or self.fields,
            tags = tags or self.tags,
            metadata = metadata or self.metadata,
            updated_at = datetime.now(),
            version = version or self.version,
            id = self.id,
            created_at = self.created_at
        )

    @property
    def full_name(self) -> str:
        return self.namespace + "/" + self.name

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "algorithm": self.algorithm,
            "namespace": self.namespace,
            "fields": {k: v.to_dict() for k, v in self.fields.items()},
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        fields = {k: SecretField.from_dict(v) for k, v in data.get("fields", {}).items()}
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            algorithm=data["algorithm"],
            namespace=data.get("namespace", ""),
            fields=fields,
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            version=data.get("version", 1)
        )

