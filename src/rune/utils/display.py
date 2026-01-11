from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.tree import Tree


console = Console()

def panel(message: str, title: str | None = None) -> None:
    console.print(Panel.fit(message, title=title))

def success_panel(message: str, title: str = "Success"):
    console.print(Panel.fit(message,title=f"[green]{title}[/]"))

def failed_panel(message: str, title: str = "Failed"):
    console.print(Panel.fit(message,title=f"[red]{title}[/]"))

def print(message: str):
    console.print(message)

def print_tree(tree: Tree):
    console.print(tree)

def print_dict(d: Dict):
    console.print(Panel.fit(Pretty(d, expand_all=True, indent_guides=True)))

