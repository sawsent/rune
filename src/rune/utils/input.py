from typing import Tuple, Dict

from rich.console import Console
from rich.panel import Panel
from rune.context import Context
from rich.prompt import Prompt

from rune.exception.badinput import BadInputError
from rune.models.crypto.namespace import Namespace

NAME_PROMPT = "Secret name"
KEY_PROMPT = "Encryption key"

def input_name() -> str:
    return Prompt.ask(NAME_PROMPT)

def input_key() -> str:
    return Prompt.ask(KEY_PROMPT, password=True)

def input_default_key() -> str:
    return Prompt.ask("The [bold]default key[/] for this session")

def sanitize_name(full_name: str) -> str:
    if "//" in full_name:
        raise BadInputError(f"Not valid name. Please input a '/'-separated name. [bold]Ex: db/prod/service[/]")
    return full_name.removeprefix("/").removesuffix("/")

def split_name_and_ns(n_and_ns: str) -> Tuple[str, Namespace]:
    s = n_and_ns.split("/")
    return s[-1], Namespace(s[:-1])

def get_secret_input(name: str) -> str:
    return Prompt.ask(f"Value for field '[bold]{name}[/]'", password=True)

def get_fields_dict(fields: str) -> Dict[str, str]:
    ret = {}
    for field in fields.split(","):
        split = field.split("=")
        if len(split) == 1:
            ret[field] = get_secret_input(field)
        elif len(split) >= 2:
            ret[split[0]] = "".join(split[1:])
    return ret

def get_fqn(name: str, namespace: Namespace) -> str:
    return "/".join(namespace.ns + [name])

def get_active_user() -> str | None:
    return Context.get().settings.active_user

def ensure_active_user() -> str:
    maybe_user = get_active_user()
    if not maybe_user:
        raise BadInputError("[bold red]User not set.[/] Please log in with [bold]`rune login -u <username>`[/]")

    return maybe_user


def require[T](arg: T | None, reason: str = "") -> T:
    if arg is None:
        raise BadInputError(reason)
    return arg


