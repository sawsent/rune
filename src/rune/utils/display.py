from rich.console import Console
from rich.panel import Panel


console = Console()

def panel(message: str, title: str | None = None) -> None:
    if not title:
        console.print(Panel.fit(message))
    else:
        console.print(Panel.fit(message, title=title))

def success_panel(message: str, title: str = "Success"):
    console.print(Panel.fit(message,title=f"[green]{title}[/]"))

def failed_panel(message: str, title: str = "Failed"):
    console.print(Panel.fit(message,title=f"[red]{title}[/]"))

