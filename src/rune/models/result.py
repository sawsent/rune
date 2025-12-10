from abc import ABC, abstractmethod
from typing import Optional

class Result[V](ABC):
    @abstractmethod
    def is_success(self) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def is_failure(self) -> bool:
        raise NotImplementedError()
    def value(self) -> Optional[V]:
        return None
    def failure_reason(self) -> Optional[str]:
        return None

class Success[V](Result[V]):
    def __init__(self, value: V = None) -> None:
        self._value = value
    def is_success(self) -> bool: return True
    def is_failure(self) -> bool: return False
    def value(self) -> Optional[V]:
        return self._value

class Failure[V](Result[V]):
    def __init__(self, failure_reason: str) -> None:
        self._failure_reason = failure_reason
    def is_success(self) -> bool: return False
    def is_failure(self) -> bool: return True

    def failure_reason(self) -> Optional[str]:
        return self._failure_reason






