from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Self

from rune.models.settings.storagesettings import StorageSettings


@dataclass
class Settings:
    encryption_algorithm: str
    storage: StorageSettings

