import os
from typing import Dict

def sanitized_env(extra: Dict[str, str] | None = None) -> Dict[str, str]:
    env = os.environ.copy()

    PYTHON_BAD = {
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTHONSTARTUP",
        "PYTHONINSPECT",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONBREAKPOINT",
        "PYTHONTRACEMALLOC",
        "PYTHONASYNCIODEBUG",
        "PYTHONWARNINGS",
    }

    LOADER_BAD = {
        "LD_PRELOAD",
        "LD_LIBRARY_PATH",
        "DYLD_INSERT_LIBRARIES",
        "DYLD_LIBRARY_PATH",
    }

    for key in PYTHON_BAD | LOADER_BAD:
        env.pop(key, None)

    for key in ("TERM", "COLUMNS", "LINES"):
        env.pop(key, None)

    if extra:
        for k, v in extra.items():
            env[k] = str(v)

    return env

