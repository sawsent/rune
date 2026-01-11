from typing import Annotated, Optional
from typer import Typer, Option

from rune.exception.session import NoSessionError, WrongUserError
from rune.utils.input import ensure_active_user, input_default_key
from rune.context import Context
from rune.utils import display

DEFAULT_KEY_HELP = (
    "Default encryption key for this session.\n"
    "If omitted, you will be prompted securely.\n"
    "The key is kept in memory only and never written to disk."
)

SESSION_TTL_HELP = (
    "Session time-to-live in seconds.\n"
    "If omitted, the configured default TTL is used.\n"
    "Use -1 to create a session that does not expire."
)

def setup() -> Typer:

    session_app = Typer(name="session", help="Manage rune session. Run `rune session -h` for more help.")
    @session_app.command(name="start")
    def start(
        _key: Annotated[
            Optional[str],
            Option("--session-key", "-k", help=DEFAULT_KEY_HELP)
        ] = None,
        _ttl: Annotated[
            Optional[int],
            Option("--ttl", help=SESSION_TTL_HELP)
        ] = None
    ):
        """
        Start a local rune session.

        A session holds a default encryption key in memory and makes it
        available to rune commands for encrypting and decrypting secrets.

        Sessions are local-only and scoped to the active username.
        """
        key = _key or input_default_key()
        username = ensure_active_user()
        context = Context.get()
        sessionmgr = context.session_manager
        ttl = _ttl or context.settings.session.default_ttl

        sessionmgr.start_session(username, key, ttl)

        expiry_message = (
            "Session will [bold]not expire[/]."
            if ttl == -1
            else f"Session will expire in [bold]{ttl} seconds[/]."
        )
        display.success_panel(
            f"Session started for user [bold cyan]{username}[/]. {expiry_message}"
        )

    @session_app.command(name="end")
    def end():
        """
        End the active session.

        This immediately clears the default encryption key from memory
        and shuts down the session daemon.
        """
        sessionmgr = Context.get().session_manager

        try:
            sessionmgr.end_session()
            display.success_panel("Session ended.")
        except NoSessionError:
            display.failed_panel("No active session to end.")


    @session_app.command(name="status")
    def status():
        """
        Show the current session status.

        Displays whether a session is running, which user it belongs to,
        and its remaining TTL (if applicable).
        """
        sessionmgr = Context.get().session_manager

        status = sessionmgr.get_session_status()
        display.success_panel(
            f"[bold]Started:[/] {status.started}\n"
            f"[bold]TTL:[/]     {status.ttl or 'N/A'}\n"
            f"[bold]User:[/]    {status.user or 'N/A'}"
        )

    return session_app

