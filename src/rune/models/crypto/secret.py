from rune.models.crypto.namespace import Namespace
from rune.models.crypto.secretfield import SecretField

from typing import Self, Dict, List
from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass
class Secret:
    full_name: str
    algorithm: str
    user: str
    fields: Dict[str, SecretField] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    deleted: bool = False

    version: int = 1

    def update(self,
               full_name: str | None = None,
               algorithm: str | None = None,
               user: str | None = None,
               fields: Dict[str, SecretField] | None = None,
               tags: List[str] | None = None,
               metadata: Dict[str, str] | None = None,
               version: int | None = None) -> Self:
        return type(self)(
            full_name = full_name or self.full_name,
            algorithm = algorithm or self.algorithm,
            user = user or self.user,
            fields = fields or self.fields,
            tags = tags or self.tags,
            metadata = metadata or self.metadata,
            updated_at = datetime.now(),
            version = version or self.version,
            id = self.id,
            created_at = self.created_at
        )

    @property
    def name_parts(self) -> List[str]:
        return self.full_name.split("/")

    @property
    def name(self) -> str:
        return self.name_parts[-1]

    @property
    def namespace(self) -> Namespace:
        return Namespace(self.name_parts[:-1])

    def soft_delete(self) -> Self:
        self.deleted = True
        return self

    def restore(self) -> Self:
        self.deleted = False
        self.fields = {k: v.restore() for k, v in self.fields.items()}
        return self

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "algorithm": self.algorithm,
            "user": self.user,
            "fields": {k: v.to_dict() for k, v in self.fields.items()},
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "deleted": self.deleted
        }

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        fields = {k: SecretField.from_dict(v) for k, v in data.get("fields", {}).items()}
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            full_name=data["full_name"],
            user = data["user"],
            algorithm=data["algorithm"],
            fields=fields,
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            version=data.get("version", 1),
            deleted=data.get("deleted", False)
        )

