from rich.tree import Tree

def dict_to_rich_tree(data: dict, label: str = "root") -> Tree:
    tree = Tree(label)

    def _add(parent: Tree, node: dict):
        for key, value in node.items():
            if isinstance(value, dict):
                branch = parent.add(f"[bold cyan]{key}[/]")
                _add(branch, value)
            elif isinstance(value, list):
                list_branch = parent.add(f"[bold green]{key}[/]")
                for item in value:
                    list_branch.add(str(item))
            else:
                parent.add(f"{key}: {value}")

    _add(tree, data)
    return tree
