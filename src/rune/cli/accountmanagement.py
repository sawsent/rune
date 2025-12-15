from typing import Annotated, Optional
import typer
from typer import Typer

from rune.commands.logincmd import handle_login_command, handle_logout_command
from rune.context import Context
from rune.commands.addcmd import handle_add_cmd
from rune.commands.getcmd import handle_get_command
from rune.commands.updatecmd import handle_update_command
from rune.commands.deletecmd import handle_delete_command
from rune.commands.listcmd import handle_ls_command
from rune.utils.input import ensure_active_user

def setup(app: Typer):
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
        Logs out of the provided username.
        The username is used to restrict access to secret namespaces.
        """
        handle_logout_command()

