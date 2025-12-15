from rich.console import Console
from rich.panel import Panel
import typer
from rune.cli import configmanagement, secretmanagement, sessionmanagement
from rune.cli import accountmanagement
from rune.context import Context
from rune.exception.badinput import BadInputError

error_management = "rethrow"

def main():
    app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
    config_app = typer.Typer(name="config", help="Manage rune configs. Run `rune config -h` for more help.")

    secretmanagement.setup(app)
    accountmanagement.setup(app)
    configmanagement.setup(config_app)

    app.add_typer(config_app)

    console = Console()

    try:
        Context.build()
        app()

    except BadInputError as e:
        console.print(Panel.fit(e.message, title="[red]Bad input[/]"))
    except RuntimeError as e:
        if error_management == "rethrow":
            raise e
        elif error_management == "print":
            print(e)
    finally:
        shutdown()

def shutdown():
    Context.get().settings_manager.save_settings(Context.get().settings)


