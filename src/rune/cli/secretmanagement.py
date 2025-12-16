from typing import Annotated, Optional
import typer
from typer import Typer

from rune.commands.addcmd import handle_add_cmd
from rune.commands.getcmd import handle_get_command
from rune.commands.updatecmd import handle_update_command
from rune.commands.deletecmd import handle_delete_command
from rune.commands.listcmd import handle_ls_command
from rune.utils.input import ensure_active_user

NAME_HELP = (
    "The name of the secret. Supports namespaces (e.g., `db/prod/my-db`). "
    "If omitted, you will be prompted."
)

FIELDS_HELP = (
    "Comma-separated fields to store. You can provide `key=value` pairs "
    "for known values. Fields without a value will be queried securely.\n"
    "Example: -f host=localhost,port=9999,user,password"
)

KEY_HELP = (
    "Encryption key to use. If omitted, the active session key will be used (if available).\n"
    "If no active session key is found, it will be queried securely."
)

KEY_HELP_UPDATE = (
    "Encryption key to use. Should be the same as the one used to originally encrypt the secret\n"
    "If omitted, the active session key will be used (if available).\n"
    "If no active session key is found, it will be queried securely."
)

def setup(app: Typer):

    @app.command()
    def add(_fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
            _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
            _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None):
        """
        Add a new secret to the vault.

        Supports namespaced secrets. Fields without explicit values
        will be prompted securely.
        """
        active_user = ensure_active_user()
        handle_add_cmd(active_user, _fields, _name, _key)
        
    @app.command()
    def delete(_name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None):
        """
        Delete a secret from the vault.

        You will be prompted if the name is omitted.
        """
        active_user = ensure_active_user()
        handle_delete_command(active_user, _name)

    @app.command()
    def update(_fields: Annotated[str, typer.Option("--fields", "-f", help=FIELDS_HELP)],
               _name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
               _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP_UPDATE)] = None):
        """
        Update an existing secret in the vault.

        Fields without explicit values will be prompted securely.
        """
        active_user = ensure_active_user()
        handle_update_command(active_user, _fields, _name, _key)

    @app.command()
    def get(_name: Annotated[Optional[str], typer.Option("--name", "-n", help=NAME_HELP)] = None,
            _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
            interactive: Annotated[bool, typer.Option(
                "--interactive", "-i",
                help="Shortcut for `rune ls -i`. Name and key are ignored when using interactive."
            )] = False,
            show: Annotated[bool, typer.Option("--show","-s",help="Show secret values in the terminal instead of hiding them.")]=False):
        """
        Retrieve a secret from the vault.

        Copies the selected field to clipboard by default.
        """
        active_user = ensure_active_user()
        if interactive:
            handle_ls_command(active_user, namespace=None, interactive=True, show=show)
        else:
            handle_get_command(active_user, _name, _key, show)

    @app.command(name="ls")
    def list_entries(namespace: Annotated[Optional[str], typer.Option("--namespace", "-ns", help="Filter secrets by namespace")] = None,
                     interactive: Annotated[bool, typer.Option("--interactive", "-i", help="Interactively select and retrieve secrets from the list.")] = False,
                     show: Annotated[bool, typer.Option("--show","-s", help="Show secret values in the terminal. Only used with --interactive.")]=False):
        """
        List all secrets in the vault for the logged in user, organized by namespace.

        Single-child namespaces are collapsed for cleaner display.
        Use `--namespace` to filter results.
        """
        active_user = ensure_active_user()
        handle_ls_command(active_user, namespace, interactive, show)

