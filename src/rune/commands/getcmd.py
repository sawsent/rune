from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import pyperclip

from rune.internal.get import get_secret
from rune.utils.input import input_key, input_name, split_name_and_ns

console = Console()

def handle_get_command(user: str, _name: str | None = None, _key: str | None = None, show: bool = False):
    name, namespace = split_name_and_ns(_name or input_name())
    key = (_key or input_key())

    result = get_secret(user, name, namespace, key)

    v = result.value()

    if not (result.is_success() and v):
        console.print(
            Panel.fit(
                f"[bold red]Error:[/] {result.failure_reason()}",
                title="[red]Failed[/]",
            )
        )
        return


    console.print(Panel.fit(
        f"Stored fields for secret '[bold cyan]{name}[/]':" + "\n" + \
        "\n".join([f"[bold cyan][{i}][/] {k}" + ("" if not show else f" - {s}") for i, (k, s) in enumerate(v.items(), 1)])
    ))

    keys = list(v.keys())

    while True:
        choice = Prompt.ask(
            "[cyan]Select field to copy[/] (q to cancel)",
        )
        if choice.lower() == "q":
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(keys):
                selected_key = keys[index]
                pyperclip.copy(v[selected_key])
                console.print(
                    Panel.fit(
                        f"[bold green]✓ Copied[/] [yellow]{selected_key}[/] to clipboard",
                        title="[green]Copied[/]",
                    )
                )
        except:
            pass


