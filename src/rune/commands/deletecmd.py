from rune.internal.delete import delete_secret, restore_secret
from rune.utils.input import input_key, input_name, sanitize_name
from rune.utils import display

def handle_delete_command(user: str, hard: bool, _name: str | None = None, _key: str | None = None) -> None:
    name = sanitize_name(_name or input_name())

    key = (_key or input_key()) if hard else ""

    result = delete_secret(user, name, hard, key)

    if result.is_success():
        display.success_panel(f"[bold green]Deleted secret[/] [cyan]{name}[/]")
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")

def handle_restore_cmd(user: str, _name: str | None) -> None:
    name = sanitize_name(_name or input_name())

    result = restore_secret(user, name)

    if result.is_success():
        display.success_panel(f"[bold green]Restored secret[/] [cyan]{name}[/]")
        return
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")

