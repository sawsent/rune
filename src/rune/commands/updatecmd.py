from rune.internal.update import update_secret
from rune.utils.input import input_key, input_name, sanitize_name, get_fields_dict
from rune.utils import display

def handle_update_command(user: str, _fields: str | None, _name: str | None, _key: str | None):

    name = sanitize_name(_name or input_name())
    fields = get_fields_dict(_fields, name)
    key = (_key or input_key())
    result = update_secret(user, name, fields, key)

    if result.is_success():
        display.success_panel(f"[bold green]Updated secret[/] [cyan]{name}[/]")
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")


