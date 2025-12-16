from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from typer import Typer, Option
from typing import Annotated, Literal, Optional

from rune.context import Context
from rune.models.settings.encryptionsettings import EncryptionSettings
from rune.models.settings.storagesettings import FileBasedStorageSettings
from rune.utils.input import require

STORAGE_MODE_HELP = "Configure how and where rune stores encrypted secrets."
STORAGE_FILE_HELP = "Where to store secrets (file) if storage mode is 'local'"

ENCRYPTION_MODE_HELP = "Configure how and where rune stores encrypted secrets."

console = Console()

def setup(app: Typer):
    @app.command(name="show")
    def show_config():
        """
        Display the rune config.
        """
        context = Context.get()
        settings_file = context.settings_manager.settings_file
        settings = context.settings.to_dict()


        console.print(f"Settings file located at: [bold]'{settings_file}'[/].")
        console.print(Pretty(settings, expand_all=True, indent_guides=True))

    @app.command(name="storage")
    def config_storage(
        _mode: Annotated[Optional[Literal["local"]], Option("--mode", "-m", help=STORAGE_MODE_HELP)] = None,
        _file: Annotated[Optional[str], Option("--file", "-f", help=STORAGE_FILE_HELP)] = None,
    ):
        """
        Configure storage for rune cli.
        """
        context = Context.get()

        mode: str = _mode or context.settings.storage.mode

        if mode == "local":
            file = require(_file, "File is required if configured mode is 'local'")
            path = Path(file)
            storage_path = str(path.expanduser().absolute())
            new_settings = FileBasedStorageSettings(storage_path)
            context.settings.update(storage=new_settings)

            console.print(Panel.fit(
                f"Changed storage file to [bold]'{storage_path}'[/].\n"
                "[dim]Note: Existing secrets are not re-encrypted.[/]",
                title="Storage file changed"
            ))

    @app.command(name="encryption")
    def config_encryption(
        mode: Annotated[Literal["aesgcm"], Option("--mode", "-m", help=ENCRYPTION_MODE_HELP)],
    ):
        """
        Configure storage for rune cli.
        """
        context = Context.get()

        if mode == context.settings.encryption.mode:
            console.print(Panel.fit(
                f"Encryption mode is already [bold]'{mode}'[/].",
                title="[red]Failed.[/]"
            ))
            return


        new_settings = EncryptionSettings.from_mode(mode)

        context.settings.update(encryption=new_settings)

        console.print(Panel.fit(
            f"Changed encryption mode to [bold]'{mode}'[/].",
            title="Encryption mode changed."
        ))

