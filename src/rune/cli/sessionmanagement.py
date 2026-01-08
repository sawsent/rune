from typing import Annotated, Optional
from typer import Typer, Argument, Option

from rune.exception.session import NoSessionError, WrongUserError
from rune.utils.input import ensure_active_user, input_default_key
from rune.context import Context
from rune.utils import display


def setup(app: Typer):
    @app.command(name="start")
    def start(
        _key: Annotated[Optional[str], Option("--default-key", "-k", help="Key")] = None,
        _ttl: Annotated[Optional[int], Option("--ttl", help="ttl")] = None
    ):
        """
        Set the active username for rune.

        The username acts as the root namespace for all secrets.
        This does not perform authentication or unlock encryption.
        """
        key = _key or input_default_key()
        username = ensure_active_user()
        context = Context.get()
        sessionmgr = context.session_manager
        ttl = _ttl or context.settings.session.default_ttl

        sessionmgr.start_session(username, key, ttl)

        expiry_message = "Session will not expire." if ttl == -1 else f"Session will expire in {ttl} seconds."
        display.success_panel(f"Session started for user [bold cyan]{username}[/]. {expiry_message}")

    @app.command(name="end")
    def end():
        """
        Clear the active username.

        After logout, no secrets can be accessed until a user is selected again.
        """
        sessionmgr = Context.get().session_manager

        try:
            sessionmgr.end_session()
            display.success_panel("Session ended.")
        except NoSessionError:
            display.failed_panel("No session started")


    @app.command(name="get")
    def get():
        """
        Clear the active username.

        After logout, no secrets can be accessed until a user is selected again.
        """
        username = ensure_active_user()
        sessionmgr = Context.get().session_manager

        try:
            key = sessionmgr.get_default_key(username)
            print(key)
        except NoSessionError:
            print("No session!")
        except WrongUserError:
            print("Wrong user!")

    @app.command(name="status")
    def status():
        """
        Clear the active username.

        After logout, no secrets can be accessed until a user is selected again.
        """
        sessionmgr = Context.get().session_manager

        status = sessionmgr.get_session_status()
        display.success_panel(f"[bold]Started:[/] {status.started}\n[bold]TTL:[/]     {status.ttl or "N/A"}\n[bold]user:[/]    {status.user or "N/A"}")




