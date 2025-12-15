from typing import Optional

from rune.utils.input import input_default_key


def handle_session_start(_default_key: Optional[str], ttl: int) -> None:
    default_key = _default_key or input_default_key()
    print(f"settings default key {default_key} with ttl {ttl}")
