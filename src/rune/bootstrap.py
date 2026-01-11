from typer import Typer

from rune.utils import display
from rune.cli import configcli, secretcli, usercli, sessioncli, profilecli
from rune.context import Context
from rune.exception.badinput import BadInputError

def main():
    app = Typer(context_settings={"help_option_names": ["-h", "--help"]})

    secretcli.setup(app)
    usercli.setup(app)

    config_app = configcli.setup()
    config_app.add_typer(profilecli.setup())

    app.add_typer(sessioncli.setup())
    app.add_typer(config_app)

    try:
        Context.build()
        app()
    except BadInputError as e:
        display.failed_panel(e.message, title="[red]Bad input[/]")
    finally:
        shutdown()

def shutdown():
    Context.get().save_settings()


