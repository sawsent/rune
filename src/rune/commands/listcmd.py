import typer

from rune.commands.getcmd import handle_get_command
from rune.internal.listsecrets import list_secrets
from rune.utils.input import split_name_and_ns

def handle_ls_command(interactive: bool):
    result = list_secrets()

    v = result.value()
    if v is not None:
        names = [secret.full_name for secret in v]
    else:
        names = []
    if result.is_success() and v is not None:
        if len(names) == 0:
            print("No secrets yet.")
        for i, name in enumerate(names, 1):
            print(f"[{i}] {name}")

    else:
        print(f"Unable to retreive secrets. Cause: {result.failure_reason()}")


    if interactive:
        while True:
            try:
                choice = typer.prompt("Select field to get (q to quit)")
                if choice == "q" or choice == "Q":
                    break
                choice = int(choice) - 1
                if 0 <= choice < len(names):
                    selected = names[choice]
                    handle_get_command(_name=selected)
                    break
            except:
                pass


