from rune.internal.get import get_secret
from rune.utils.input import get_choice_by_idx, input_key, input_name, sanitize_name
from rune.utils import display

import pyperclip


def handle_get_command(user: str, _name: str | None = None, _key: str | None = None, show: bool = False, show_deleted: bool = False):
    name = sanitize_name(_name or input_name())
    key = (_key or input_key())

    result = get_secret(user, name, key)

    v = result.value()

    if not (result.is_success() and v):
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")
        return
    
    to_display = {k:s[0] for k, s in v.items() if show_deleted or not s[1]}

    display.panel(
        f"Stored fields for secret '[bold cyan]{name}[/]':\n" + \
        "\n".join([f"[bold cyan][{i}][/] {k}" + ("" if not show else f" - {s}") for i, (k, s) in enumerate(to_display.items(), 1)])
    )

    choice = get_choice_by_idx("[cyan]Select field to copy[/]", list(v.keys()))
    if not choice:
        return

    pyperclip.copy(choice)
    display.success_panel(f"[bold green]✓ Copied to clipboard[/]", title="Copied")

