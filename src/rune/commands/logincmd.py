from rune.context import Context
from rune.utils import display


def handle_login_command(username: str) -> None:
    Context.get().settings.update(active_user=username)
    display.success_panel(f"Logged in as [bold]'{username}'[/]")

def handle_logout_command() -> None:
    active_user = Context.get().settings.active_user

    if not active_user:
        display.failed_panel("Not logged in")
        return

    Context.get().settings.reset(active_user=True)

    display.success_panel("Successfully logged out")



