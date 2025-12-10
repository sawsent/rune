from typing import Annotated, Literal, Optional, Tuple
import typer
import pyperclip

from rune.internal.add import add_secret
from rune.internal.delete import delete_secret
from rune.internal.get import get_secret
from rune.internal.listsecrets import list_secrets
from rune.internal.update import update_secret
from rune.utils.settings import ensure_secrets_exist, ensure_settings_exist, get_secrets_path, get_settings_path, update_settings

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

NAME_HELP = "The name of the new secret (will be prompted for if not provided)"
SECRET_HELP = "Secret text (will be prompted for if not provided)"
KEY_HELP = "Encryption key (will be prompted for if not provided)"

NAME_PROMPT = "The name of the secret"
SECRET_PROMPT = "The secret"
KEY_PROMPT = "The encryption key for this secret"

def enrich_arguments(name: Optional[str] = "",
                     secret: Optional[str] = "",
                     key: Optional[str] = "") -> Tuple[str, str, str]:
    if name is None:
        name = typer.prompt(NAME_PROMPT)
    if secret is None:
        secret = typer.prompt(SECRET_PROMPT, hide_input=True)
    if key is None:
        key = typer.prompt(KEY_PROMPT, hide_input=True)

    if name is not None and secret is not None and key is not None:
        return (name, secret, key)
    return ("", "", "")

@app.command()
def add(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
        secret: Annotated[Optional[str], typer.Option("--secret", "-s", help=SECRET_HELP)] = None,
        key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Add a secret to the rune vault.
    """
    name, secret, key = enrich_arguments(name=name, secret=secret, key=key)
    result = add_secret(name, secret, key)

    if result.is_success():
        print(f"Stored new secret {name}")
    else:
        print(result.failure_reason())
    

@app.command()
def delete(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None):
    """
    Removes a secret from the rune vault.
    """
    name, _, _ = enrich_arguments(name=name)
    result = delete_secret(name)
    if result.is_success() is None:
        print(f"Deleted secret {name}")
    else:
        print(result.failure_reason())

@app.command()
def update(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
           secret: Annotated[Optional[str], typer.Option("--secret", "-s", help=SECRET_HELP)] = None,
           key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Update a secret in the rune vault.
    """
    name, secret, key = enrich_arguments(name=name, secret=secret, key=key)
    result = update_secret(name, secret, key)
    if result.is_success():
        print(f"Updated secret {name}")
    else:
        print(result.failure_reason())



@app.command()
def get(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
        key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
        show_secret: Annotated[bool, typer.Option("--show", help="Display the secret to the terminal")] = False):
    """
    Retreive a secret from the rune vault.

    Will copy it directly to the clipboard.
    Use --show to also show it to the terminal.
    """
    name, _, key = enrich_arguments(name=name, key=key)
    result = get_secret(name, key)

    v = result.value()
    if result.is_success() and v is not None:
        pyperclip.copy(v)
        print("Secret copied to clipboard")
        if show_secret:
            print(f"Secret: {v}")
    else:
        print(result.failure_reason())

@app.command()
def list():
    """
    Lists all secret names from the rune vault.
    """
    result = list_secrets()

    v = result.value()
    if result.is_success() and v is not None:
        if len(v) == 0:
            print("No secrets yet.")
        for i, s in enumerate(v):
            print(f"[{i + 1}] {s.name}")
    else:
        print(f"Unable to retreive secrets. Cause: {result.failure_reason()}")

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

