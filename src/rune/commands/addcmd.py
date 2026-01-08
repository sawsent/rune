from rune.internal.add import add_secret
from rune.utils.input import get_session_key, input_key, input_name, sanitize_name, get_fields_dict
from rune.utils import display

def handle_add_cmd(user: str, _fields: str | None, _name: str | None, _key: str | None, use_session_key: bool):
    name = sanitize_name(_name or input_name())
    fields = get_fields_dict(_fields, name)

    session_key = get_session_key(user) if use_session_key else None
    key = _key or session_key or input_key()

    result = add_secret(user, name, fields, key)

    if result.is_success():
        display.success_panel(f"[bold green]✓ Stored new secret[/] [cyan]{name}[/]")
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")


