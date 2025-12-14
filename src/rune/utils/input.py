from typing import Tuple, Dict
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
    return s[-1], "/".join(s[:-1]).removeprefix("/").removesuffix("/").strip()

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

def get_fqn(name: str, namespace: str) -> str:
    if namespace == "":
        return name
    else:
        return namespace + "/" + name




