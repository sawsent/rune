from typing import Annotated, Optional
import typer

from rune.commands.addcmd import handle_add_cmd
from rune.commands.getcmd import handle_get_command
from rune.commands.updatecmd import handle_update_command
from rune.commands.deletecmd import handle_delete_command
from rune.commands.listcmd import handle_ls_command

from rune.utils.settings import ensure_secrets_exist, ensure_settings_exist

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

NAME_HELP = (
    "The name of the new secret.\n"
        "Supports namespaces (e.g. `db/prod/my-db`). If omitted, you'll be prompted."
)

FIELDS_HELP = (
    "Fields to store, comma-separated. Example: `-f host,port,user,password`.\n"
        "Each field will be queried securely."
)

KEY_HELP = "Encryption key (if omitted, will be securely prompted)."

@app.command()
def add(
    _fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
    _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
):
    """
    Add a secret to the rune vault.
    """
    handle_add_cmd(_fields, _name, _key)
    
@app.command()
def delete(
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None
):
    """
    Removes a secret from the rune vault.
    """
    handle_delete_command(_name)
    
@app.command()
def update(
    _fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
    _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
):
    """
    Update an existing secret in the rune vault.
    """
    handle_update_command(_fields, _name, _key)

@app.command()
def get(
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
    _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
    show: Annotated[bool, typer.Option("--show","-s",help="Show the secret values instead of hiding them.")] = False,
):
    """
    Retrieve a secret from the rune vault.

    Copies the selected field to clipboard.
    Use --show to display field values in the terminal.
    """
    handle_get_command(_name, _key, show)

@app.command(name="ls")
def list_entries(
    interactive: Annotated[
    bool,
    typer.Option(
        "--interactive",
        "-i",
        help="Interactively select and retrieve secrets from the list.",
    ),
] = False
):
    """
    Lists all secrets in the rune vault, organized by namespace.
    Collapses single-child namespaces for cleaner display.
    """
    handle_ls_command(interactive)

def main():
    ensure_settings_exist()
    ensure_secrets_exist()
    app()

