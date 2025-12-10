from typing import Annotated, Optional, Tuple
import typer

from rune.internal.add import add_secret
from rune.internal.listsecrets import list_secrets
from rune.utils.settings import ensure_settings_exist

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

NAME_HELP = "The name of the new secret (will be prompted for if not provided)"
SECRET_HELP = "Secret text (will be prompted for if not provided)"
KEY_HELP = "Encryption key (will be prompted for if not provided)"

NAME_PROMPT = "The name of the secret"
SECRET_PROMPT = "The secret"
KEY_PROMPT = "The encryption key for this secret (REMEMBER THIS OR YOUR SECRET WILL BE LOST)"

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
    add_secret(name, secret, key)
    

@app.command()
def delete(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None):
    """
    Removes a secret from the rune vault.
    """
    name, _, _ = enrich_arguments(name=name)
    print(name)

@app.command()
def update(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
           secret: Annotated[Optional[str], typer.Option("--secret", "-s", help=SECRET_HELP)] = None,
           key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Update a secret in the rune vault.
    """
    name, secret, key = enrich_arguments(name=name, secret=secret, key=key)
    print(name)
    print(secret)
    print(key)

@app.command()
def get(name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
        key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
    """
    Retreive a secret from the rune vault.
    """
    name, _, key = enrich_arguments(name=name, key=key)
    print(name)
    print(key)

@app.command()
def list():
    """
    Lists all secret names from the rune vault.
    """
    list_secrets()

def main():
    ensure_settings_exist()
    app()

