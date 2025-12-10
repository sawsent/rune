from typing import Annotated, Dict, List, Literal, Optional, Tuple
import typer
import pyperclip

from rune.internal.add import add_secret
from rune.internal.delete import delete_secret
from rune.internal.get import get_secret
from rune.internal.listsecrets import list_secrets
from rune.internal.update import update_secret
from rune.utils.settings import ensure_secrets_exist, ensure_settings_exist, get_secrets_path, get_settings_path, update_settings

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

NAME_HELP = "The name of the new secret (will be prompted for if not provided). You can organize items in namespaces (eg. `db/prod/my-production-database`)"
FIELDS_HELP = "The fields to store. Usage `-f host,port,username,password`. They will be queried secretly."
KEY_HELP = "Encryption key (will be prompted for if not provided)"

NAME_PROMPT = "The name of the secret"
SECRET_PROMPT = "The secret"
KEY_PROMPT = "The encryption key for this secret"

def enrich_arguments(name: Optional[str] = "",
                     key: Optional[str] = "") -> Tuple[str, str, str]:
    namespace = ""
    name_and_space = (name or typer.prompt(NAME_PROMPT)).split("/")
    if len(name_and_space) == 0:
        raise ValueError("Name must have at least 1 character")
    if len(name_and_space) == 1:
        name = name_and_space[0]
    else:
        name = name_and_space[-1]
        namespace = "/".join(name_and_space[:-1]).removeprefix("/").removesuffix("/").strip()

    if key is None:
        key = typer.prompt(KEY_PROMPT, hide_input=True)

    if name is not None and key is not None:
        return (name, namespace, key)
    return ("", "", "")

def get_secret_input(name: str) -> str:
    key = typer.prompt(f"The value for field '{name}'", hide_input=True)
    return key

def get_fields_dict(fields: str) -> Dict[str, str]:
    return {k: get_secret_input(k) for k in fields.split(",")}


@app.command()
def add(fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
        name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
        key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Add a secret to the rune vault.
    """
    fields_dict = get_fields_dict(fields)
    name, namespace, key = enrich_arguments(name=name, key=key)

    result = add_secret(name, fields_dict, key, namespace)
    if result.is_success():
        print(f"Stored new secret {name}")
    else:
        print(result.failure_reason())


@app.command()
def delete(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None):
    """
    Removes a secret from the rune vault.
    """
    name, namespace, _ = enrich_arguments(name=name)
    result = delete_secret(name, namespace)
    if result.is_success() is None:
        print(f"Deleted secret {name}")
    else:
        print(result.failure_reason())

@app.command()
def update(fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
           name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
           key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Update a secret in the rune vault.
    """

    fields_dict = get_fields_dict(fields)
    name, namespace, key = enrich_arguments(name=name, key=key)
    result = update_secret(name, fields_dict, key, namespace)
    if result.is_success():
        print(f"Updated secret {name}")
    else:
        print(result.failure_reason())

@app.command()
def get(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
        key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
        show: Annotated[bool, typer.Option("--show", "-s", help="Show the secrets when retreived.")] = False):
    """
    Retreive a secret from the rune vault.

    Will copy it directly to the clipboard.
    Use --show to also show it to the terminal.
    """
    name, namespace, key = enrich_arguments(name=name, key=key)
    result = get_secret(name, key, namespace)

    v = result.value()
    if result.is_success() and v is not None:
        for i, (k, s) in enumerate(v.items(), 1):
            print(f"[{i}] - {k}{f": {s}" if show else ""}")

        keys = list(v.keys())

        while True:
            try:
                choice = typer.prompt("Select field to copy (q to cancel)")
                if choice == "q" or choice == "Q":
                    print("No secret copied")
                    break
                choice = int(choice) - 1
                if 0 <= choice < len(keys):
                    selected_key = keys[choice]
                    pyperclip.copy(v[selected_key])
                    print(f"'{selected_key}' copied to clipboard!")
                    break
            except:
                pass

    else:
        print(result.failure_reason())

@app.command(name="ls")
def list_entries(interactive: Annotated[bool, typer.Option("--interactive", "-i", help="Wether the list is interactive (you can query secrets from ls)")] = False):
    """
    Lists all secret names from the rune vault.
    """
    result = list_secrets()

    v = result.value()
    if v is not None:
        names = [secret.full_name for secret in v]
    else:
        names = []
    if result.is_success() and v is not None:
        if len(names) == 0:
            print("No secrets yet.")
        for i, name in enumerate(names, 1):
            print(f"[{i}] {name}")

    else:
        print(f"Unable to retreive secrets. Cause: {result.failure_reason()}")


    if interactive:
        while True:
            try:
                choice = typer.prompt("Select field to get (q to quit)")
                if choice == "q" or choice == "Q":
                    break
                choice = int(choice) - 1
                if 0 <= choice < len(names):
                    selected = names[choice]
                    get(selected)
                    break
            except:
                pass


@app.command()
def config(encryption: Annotated[Optional[Literal["no-encryption", "aesgcm"]], typer.Option("--encryption", "-e", help="The type of encryption.")] = None,
           storage_mode: Annotated[Optional[Literal["local"]], typer.Option("--storage-mode", "-s", help="Storage mode.")] = None,
           secrets_location: Annotated[Optional[str], typer.Option("--secrets-file", "-f", help="Where to store secrets (Ex: ~/.secrets.json).")] = None):
    """
    Configure rune.

    Use rune config -h for more help.
    """

    if all([(x is None) for x in [encryption, storage_mode, secrets_location]]):
        print("Please specify at least one option to configure")
        return

    result = update_settings(encryption=encryption, storage_mode=storage_mode, storage_file=secrets_location)
    if result.is_success():
        print(result.value())
    else:
        print(result.failure_reason())

@app.command()
def whereis():
    """
    Show the location of the settings file and the secrets file
    """
    print(f"settings: {get_settings_path()}")
    print(f"secrets:  {get_secrets_path()}")

def main():
    ensure_settings_exist()
    ensure_secrets_exist()
    app()

