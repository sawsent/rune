from rich.console import Console
from rich.panel import Panel

from rune.internal.delete import delete_secret
from rune.utils.input import input_name, split_name_and_ns

console = Console()

def handle_delete_command(_name: str | None = None) -> None:
    name, namespace = split_name_and_ns(_name or input_name())
    result = delete_secret(name, namespace)

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


