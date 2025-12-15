from typing import Annotated, Optional
import typer

from rune.commands.logincmd import handle_login_command, handle_logout_command
from rune.context import Context
from rune.commands.addcmd import handle_add_cmd
from rune.commands.getcmd import handle_get_command
from rune.commands.updatecmd import handle_update_command
from rune.commands.deletecmd import handle_delete_command
from rune.commands.listcmd import handle_ls_command
from rune.utils.input import ensure_active_user

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

NAME_HELP = (
    "The name of the new secret.\n"
        "Supports namespaces (e.g. `db/prod/my-db`). If omitted, you'll be prompted."
)

FIELDS_HELP = (
    "Fields to store, comma-separated. Example: `-f host=localhost,port=9999,user,password`.\n"
        "Each field will be queried securely if not provided."
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
    _active_user = ensure_active_user()
    handle_add_cmd(_active_user, _fields, _name, _key)
    
@app.command()
def delete(
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None
):
    """
    Removes a secret from the rune vault.
    """
    _active_user = ensure_active_user()
    handle_delete_command(_active_user, _name)

@app.command()
def update(
    _fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
    _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
):
    """
    Update an existing secret in the rune vault.
    """
    _active_user = ensure_active_user()
    handle_update_command(_active_user, _fields, _name, _key)

@app.command()
def get(
    _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
    _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
    interactive: Annotated[bool, typer.Option(
        "--interactive", "-i",
        help="Interactively select and retrieve secrets from the list. (same as running `rune ls -i`). Name and key are discarded."
    )] = False,
    show: Annotated[bool, typer.Option("--show","-s",help="Show the secret values instead of hiding them.")] = False,
):
    """
    Retrieve a secret from the rune vault.

    Copies the selected field to clipboard.
    Use --show to display field values in the terminal.
    """
    _active_user = ensure_active_user()
    if interactive:
        handle_ls_command(_active_user, None, interactive, show)
    else:
        handle_get_command(_active_user, _name, _key, show)

@app.command(name="ls")
def list_entries(
    namespace: Annotated[Optional[str], typer.Option("--namespace", "-ns", help="Filter the shown secrets by namespace")] = None,
    interactive: Annotated[bool, typer.Option("--interactive", "-i", help="Interactively select and retrieve secrets from the list.")] = False,
    show: Annotated[bool, typer.Option(
        "--show","-s",
        help="Show the secret values instead of hiding them. Only used when running with the --interactive flag."
    )] = False,
):
    """
    Lists all secrets in the rune vault, organized by namespace.
    Collapses single-child namespaces for cleaner display.
    """
    _active_user = ensure_active_user()
    handle_ls_command(_active_user, namespace, interactive, show)

@app.command(name="login")
def login(
    username: Annotated[str, typer.Argument(help="The username to login with.")],
):
    """
    Logs in with the provided name.
    The username is used to restrict access to secret namespaces.
    """
    handle_login_command(username)

@app.command(name="logout")
def logout():
    """
    Logs in with the provided name.
    The username is used to restrict access to secret namespaces.
    """
    handle_logout_command()




def main():
    Context.build()
    try:
        app()
    except RuntimeError as e:
        raise e
    finally:
        shutdown()

def shutdown():
    Context.get().settings_manager.save_settings(Context.get().settings)





