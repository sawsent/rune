from typing import Optional, Tuple, Dict
from rich.prompt import Prompt

NAME_PROMPT = "Secret name"
KEY_PROMPT = "Encryption key"

def input_name() -> str:
    return Prompt.ask(NAME_PROMPT)

def input_key() -> str:
    return Prompt.ask(KEY_PROMPT, password=True)

def split_name_and_ns(n_and_ns: str) -> Tuple[str, str]:
    s = n_and_ns.split("/")
    if len(s) == 1:
        return (s[0], "")
    return s[-1], "/".join(s[:-1]).removeprefix("/").removesuffix("/")

def get_secret_input(name: str) -> str:
    return Prompt.ask(f"Value for field '[bold]{name}[/]'", password=True)

def get_fields_dict(fields: str) -> Dict[str, str]:
    return {k.strip(): get_secret_input(k.strip()) for k in fields.split(",")}


