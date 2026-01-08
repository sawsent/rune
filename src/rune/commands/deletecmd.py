from rune.internal.delete import delete_secret, delete_secret_fields, restore_secret
from rune.utils.input import get_fields_keys, get_session_key, input_key, input_name, sanitize_name
from rune.utils import display

def handle_delete_command(user: str, hard: bool, _name: str | None, _key: str | None, use_session_key: bool) -> None:
    name = sanitize_name(_name or input_name())

    session_key = get_session_key(user) if use_session_key else None
    key = _key or session_key or input_key()

    result = delete_secret(user, name, hard, key)

    if result.is_success():
        display.success_panel(f"[bold green]Deleted secret[/] [cyan]{name}[/]")
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")

def handle_delete_fields_command(user: str, hard: bool, _name: str | None, _key: str | None, _fields: str, use_session_key: bool) -> None:
    name = sanitize_name(_name or input_name())
    fields = get_fields_keys(_fields)

    session_key = get_session_key(user) if use_session_key else None
    key = _key or session_key or input_key()

    result = delete_secret_fields(user, name, hard, key, fields)

    if result.is_success():
        display.success_panel(f"[bold green]Deleted secret fields {", ".join(fields)}[/] for secret [cyan]{name}[/]")
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

