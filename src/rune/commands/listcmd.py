from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
import typer
from rune.commands.getcmd import handle_get_command
from rune.internal.listsecrets import list_secrets
from rich.console import Console
from rich.tree import Tree
import typer

console = Console()

def handle_ls_command(user: str, namespace: str | None, interactive: bool, show: bool, show_deleted: bool):
    result = list_secrets(user)
    secrets = result.value()

    if result.is_failure():
        console.print(Panel.fit(
            f"[bold red]Unable to retrieve secrets:[/] {result.failure_reason()}",
            title="[red]Failed[/]",
        ))
        return

    if not secrets:
        console.print("[yellow]No secrets yet.[/]")
        return
    
    if show_deleted:
        full_names = []
        for secret in secrets:
            fn = secret.full_name
            if secret.deleted:
                parts = fn.split("/")
                parts[-1] = parts[-1] + " (deleted)"
                full_names.append("/".join(parts))
            else:
                full_names.append(fn)
    else:
        full_names = [secret.full_name for secret in secrets if not secret.deleted]

    if not full_names:
        console.print("[yellow]No secrets yet.[/]")
        return

    names_tree = _build_namespace_tree(full_names)

    if namespace:
        for ns in namespace.split("/"):
            if ns != "":
                names_tree = names_tree.get(ns, {})

    if names_tree == {}:
        console.print(f"[yellow]No secrets for namespace {namespace}.[/]")
        return

    compacted_tree = _compact_tree(names_tree)

    root = Tree(f"[bold]{user}/{namespace}/[/]" if namespace else f"[bold]{user}/[/]")
    indexes = _expand_rich_tree(root, compacted_tree)
    console.print(
        Panel.fit(
            root,
            title="[green]✓ Secrets Tree[/]"
        )
    )

    if interactive:
        while True:
            choice = typer.prompt("Select secret to get (q to quit)")
            if choice.lower() == "q":
                break

            try:
                idx = int(choice)
            except:
                continue
            if idx in indexes:
                if namespace:
                    fqn = namespace.removeprefix("/").removesuffix("/").strip() + "/" + indexes[idx]
                else:
                    fqn = indexes[idx]
                console.print(f"Fetching secret [bold]{fqn}[/]")
                handle_get_command(user, _name=fqn, show=show)
                break


def _build_namespace_tree(full_names: List[str]) -> Dict:
    def _build_branch(current: Dict, parts: List[str]) -> Dict:
        if len(parts) == 1:
            if not "__items__" in current:
                current["__items__"] = []
            current["__items__"].append(parts[0])
            return current

        if not parts[0] in current:
            current[parts[0]] = {}

        current[parts[0]] = _build_branch(current.get(parts[0], {}), parts[1:])
        return current

    
    tree = {}
    for path in full_names:
        tree = _build_branch(tree, path.split("/"))

    return tree

def _expand_rich_tree(tree: Tree, node: dict, sorted_item_list: List[str] = [], current_path: str | None = None) -> Dict[int, str]:
    """Recursively expand the namespace tree into a Rich Tree."""
    items = node.get("__items__", [])
    for item in items:
        tree.add(f"[bold cyan][{len(sorted_item_list) + 1}][/] {item.replace("(deleted)", "[bold red][DELETED][/]")}")
        full_name = item if current_path is None else current_path + "/" + item
        sorted_item_list.append(full_name)

    for key, value in node.items():
        if key == "__items__":
            continue
        subtree = tree.add(f"[bold]{key}/[/]")
        full_path = key if not current_path else current_path + "/" + key
        _expand_rich_tree(subtree, value, sorted_item_list, full_path)

    return {idx: item for idx, item in enumerate(sorted_item_list, 1)}

def _compact_tree(node: Dict) -> Dict:
    compacted = {}
    for key, child in node.items():
        if key == "__items__":
            compacted[key] = list(child)
        else:
            compacted[key] = _compact_tree(child)

    result = {}

    for key, child in list(compacted.items()):
        if key == "__items__":
            result.setdefault("__items__", []).extend(child)
            continue

        current_key = key
        current_child = child

        while True:
            if not isinstance(current_child, dict):
                break

            child_items = current_child.get("__items__", [])
            ns_children = [k for k in current_child.keys() if k != "__items__"]

            if child_items:
                break
            if len(ns_children) != 1:
                break

            next_key = ns_children[0]
            next_child = current_child[next_key]

            current_key = f"{current_key}/{next_key}"
            current_child = next_child

        result[current_key] = current_child

    result.setdefault("__items__", [])
    return result

