from rich.console import Console
from rich.panel import Panel
from rune.internal.add import add_secret
from rune.utils.input import input_key, input_name, sanitize_name, get_fields_dict

console = Console()

def handle_add_cmd(user: str, _fields: str, _name: str | None = None, _key: str | None = None):
    name = sanitize_name(_name or input_name())
    fields = get_fields_dict(_fields)
    key = _key or input_key()

    result = add_secret(user, name, fields, key)

    if result.is_success():
        console.print(
            Panel.fit(
                f"[bold green]✓ Stored new secret[/] [cyan]{name}[/]",
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


