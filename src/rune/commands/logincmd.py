from rich.console import Console
from rich.panel import Panel
from rune.context import Context


def handle_login_command(username: str) -> None:
    Context.get().settings.update(active_user=username)

    console = Console()

    console.print(Panel.fit(
        f"Logged in as [bold]'{username}'[/]",
        title="[green]Success[/]"
    ))

def handle_logout_command() -> None:
    active_user = Context.get().settings.active_user

    console = Console()

    if not active_user:
        console.print(Panel.fit(
            f"Not logged in.",
            title="[red]Failed[/]"
        ))
        return


    Context.get().settings.reset(active_user=True)

    console.print(Panel.fit(
        f"Successfuly logged out",
        title="[green]Success[/]"
    ))



