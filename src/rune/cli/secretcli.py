from typing import Annotated, Optional
import typer
from typer import Typer

from rune.commands.addcmd import handle_add_cmd
from rune.commands.getcmd import handle_get_command
from rune.commands.movecmd import handle_move_command
from rune.commands.updatecmd import handle_update_command
from rune.commands.deletecmd import handle_delete_command, handle_delete_fields_command, handle_restore_cmd
from rune.commands.listcmd import handle_ls_command
from rune.utils.input import ensure_active_user

NAME_HELP = (
    "The name of the secret. Supports namespaces (e.g., `db/prod/my-db`). "
    "If omitted, you will be prompted."
)

FIELDS_HELP = (
    "Comma-separated fields to store. You can provide `key=value` pairs "
    "for known values. Fields without a value will be queried securely.\n"
    "If omitted, will store a single-field secret where the field has the same name as the secret.\n"
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
    def add(
        _name: Annotated[Optional[str], typer.Argument(help=NAME_HELP)] = None,
        _fields: Annotated[Optional[str], typer.Option("--fields", "-f", help=FIELDS_HELP)] = None,
        _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
        no_session_key: Annotated[bool, typer.Option("--no-session-key", help="Use --no-session-key to force encryption key input.")] = False,
    ):
        """
        Add a new secret to the vault.

        Supports namespaced secrets. Fields without explicit values
        will be prompted securely.
        """
        active_user = ensure_active_user()
        handle_add_cmd(active_user, _fields, _name, _key, not no_session_key)

    @app.command()
    def delete(
        _name: Annotated[Optional[str], typer.Argument(help=NAME_HELP)] = None,
        _fields: Annotated[
            Optional[str], 
            typer.Option("--fields", "-f", help="The fields to delete. Will delete all fields if not provided. Ex: -f <field1>,<field2>")
        ] = None,
        _hard: Annotated[bool, typer.Option("--hard", help="Hard delete the secret. Requires encryption key.")] = False,
        _key: Annotated[Optional[str], typer.Option("--key", "-k", help="Key used to encrypt the secret. Required if `--hard`.")] = None,
        no_session_key: Annotated[bool, typer.Option("--no-session-key", help="Use --no-session-key to force encryption key input.")] = False,
    ):
        """
        Delete a secret from the vault.

        Hard delete requires original encryption key.
        """
        active_user = ensure_active_user()
        if not _fields:
            handle_delete_command(active_user, _hard, _name, _key, not no_session_key)
        else:
            handle_delete_fields_command(active_user, _hard, _name, _key, _fields, not no_session_key)

    @app.command()
    def restore(
        _name: Annotated[Optional[str], typer.Argument(help=NAME_HELP)] = None
    ):
        """
        Restore a soft deleted secret.
        """
        active_user = ensure_active_user()
        handle_restore_cmd(active_user, _name)


    @app.command()
    def update(
        _name: Annotated[Optional[str], typer.Argument(help=NAME_HELP)] = None,
        _fields: Annotated[Optional[str], typer.Option("--fields", "-f", help=FIELDS_HELP)] = None,
        _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP_UPDATE)] = None,
        no_session_key: Annotated[bool, typer.Option("--no-session-key", help="Use --no-session-key to force encryption key input.")] = False,
    ):
        """
        Update an existing secret in the vault.

        Fields without explicit values will be prompted securely.
        """
        active_user = ensure_active_user()
        handle_update_command(active_user, _fields, _name, _key, not no_session_key)

    @app.command()
    def get(
        _name: Annotated[Optional[str], typer.Argument(help=NAME_HELP)] = None,
        _key: Annotated[Optional[str], typer.Option("--key", "-k", help=KEY_HELP)] = None,
        show: Annotated[bool, typer.Option("--show","-s",help="Show secret values in the terminal instead of hiding them.")]=False,
        show_deleted: Annotated[bool, typer.Option("--show-deleted", help="Show soft deleted fields")]=False,
        no_session_key: Annotated[bool, typer.Option("--no-session-key", help="Use --no-session-key to force encryption key input.")] = False,
    ):
        """
        Retrieve a secret from the vault.

        Copies the selected field to clipboard by default.
        """
        active_user = ensure_active_user()
        handle_get_command(active_user, _name, _key, show, show_deleted, not no_session_key)

    OG_NAME_HELP = "Full name of secret to move"
    DEST_NAME_HELP = "Destination name for the secret"
    @app.command(name="move")
    def move(
        _original_name: Annotated[Optional[str], typer.Argument(help=OG_NAME_HELP)] = None,
        _new_name: Annotated[Optional[str], typer.Argument(help=DEST_NAME_HELP)] = None
    ):
        """
        Move a secret from one name to another.
        """
        active_user = ensure_active_user()
        handle_move_command(active_user, _original_name, _new_name)

    @app.command(name="ls")
    def list_entries(
        namespace: Annotated[Optional[str], typer.Argument(help="Filter secrets by namespace")] = None,
        interactive: Annotated[bool, typer.Option("--interactive", "-i", help="Interactively select and retrieve secrets from the list.")] = False,
        show: Annotated[bool, typer.Option("--show","-s", help="Show secret values in the terminal. Only used with --interactive.")]=False,
        show_deleted: Annotated[bool, typer.Option("--show-deleted", help="Show soft deleted secrets.")] = False,
        no_session_key: Annotated[bool, typer.Option("--no-session-key", help="Use --no-session-key to force encryption key input.")] = False,
    ):
        """
        List all secrets in the vault for the logged in user, organized by namespace.

        Single-child namespaces are collapsed for cleaner display.
        Use `--namespace` to filter results.
        """
        active_user = ensure_active_user()
        handle_ls_command(active_user, namespace, interactive, show, show_deleted, not no_session_key)

