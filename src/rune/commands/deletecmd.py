from rune.internal.delete import delete_secret
from rune.utils.input import input_name, sanitize_name

from rich.console import Console
from rich.panel import Panel

console = Console()

def handle_delete_command(user: str, _name: str | None = None) -> None:
    name = sanitize_name(_name or input_name())
    result = delete_secret(user, name)

    if result.is_success():
        console.print(
            Panel.fit(
                f"[bold green]✓ Deleted secret[/] [cyan]{name}[/]",
                title="[green]Success[/]",
            )
        )
    else:
        console.print(
            Panel.fit(
                f"[bold red]Error:[/] {result.failure_reason()}",
                title="[red]Failed[/]",
            )
        )


