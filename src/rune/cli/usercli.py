from typing import Annotated
from typer import Typer, Argument

from rune.commands.logincmd import handle_login_command, handle_logout_command

def setup(app: Typer):
    @app.command(name="login")
    def login(
        username: Annotated[
            str,
            Argument(help="Set the active username (namespace root).")
        ],
    ):
        """
        Set the active username for rune.

        The username acts as the root namespace for all secrets.
        This does not perform authentication or unlock encryption.
        """
        handle_login_command(username)


    @app.command(name="logout")
    def logout():
        """
        Clear the active username.

        After logout, no secrets can be accessed until a user is selected again.
        """
        handle_logout_command() 
