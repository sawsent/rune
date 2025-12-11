from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rune.internal.update import update_secret
from rune.utils.input import input_key, input_name, split_name_and_ns, get_fields_dict

console = Console()

def handle_update_command(_fields: str, _name: str | None = None, _key: str | None = None):

    name, namespace = split_name_and_ns(_name or input_name())
    fields = get_fields_dict(_fields)
    key = (_key or input_key())
    result = update_secret(name, fields, key, namespace)

    if result.is_success():
        console.print(
            Panel.fit(
                f"[bold green]✓ Updated secret[/] [cyan]{name}[/]",
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


