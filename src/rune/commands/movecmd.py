from rich.prompt import Prompt

from rune.internal.move import move_secret
from rune.utils.input import sanitize_name
from rune.utils import display

def handle_move_command(user: str, _original_name: str | None, _new_name: str | None):
    original_name = sanitize_name(_original_name or Prompt.ask("The name of the secret you want to move"))
    new_name = sanitize_name(_new_name or Prompt.ask("The new name of the secret"))

    result = move_secret(user, original_name, new_name)

    if result.is_success():
        display.success_panel(f"Secret '[bold cyan]{original_name}[/]' was moved to '[bold cyan]{new_name}[/]'.")
    else:
        display.failed_panel(f"[bold red]Error:[/] {result.failure_reason()}")


