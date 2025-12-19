from rich.console import Console
from rich.panel import Panel


console = Console()

def success_panel(message: str, title: str = "Success"):
    console.print(Panel.fit(
        message,
        title=f"[green]{title}[/]",
    ))

def failed_panel(message: str, title: str = "Failed"):
    console.print(Panel.fit(
        message,
        title=f"[red]{title}[/]",
    ))

