from typer import Typer, Option
from typing import Annotated, Optional

from rune.commands.session import handle_session_start

DEFAULT_KEY_HELP = "The default key for this session. Will be used if no specific key is provided throughout the session."
TTL_HELP = "Seconds before default key expires. -1 means it will not expire"

def setup(app: Typer):
    @app.command(name="start")
    def start_session(
        _default_key: Annotated[Optional[str], Option("--default-key", "-k", help=DEFAULT_KEY_HELP)] = None,
        ttl: Annotated[int, Option("--ttl", "-t", help=TTL_HELP)] = -1,
    ):
        """
        Starts a session with the provided default key.

        The default key will be used if no specific key is provided when creating/retreiving secrets.
        """
        handle_session_start(_default_key, ttl)


