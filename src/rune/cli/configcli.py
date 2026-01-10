from pathlib import Path
from typer import Argument, Typer, Option
from typing import Annotated, Literal, Optional
import pyperclip

from rune.context import Context
from rune.models.settings.encryptionsettings import EncryptionSettings
from rune.models.settings.sessionsettings import DaemonSessionSettings
from rune.models.settings.storagesettings import FileBasedStorageSettings
from rune.utils.input import get_choice_by_idx, require
from rune.utils import display

STORAGE_MODE_HELP = (
    "Configure how rune stores encrypted secrets.\n"
    "Currently supported modes:\n"
    "  - local: store secrets in a local file on disk."
)

STORAGE_FILE_HELP = (
    "Path to the secrets file when using local storage.\n"
    "Example: ~/.rune/secrets.json"
)

ENCRYPTION_MODE_HELP = (
    "Configure the encryption algorithm used to encrypt secrets.\n"
    "Changing this does NOT re-encrypt existing secrets."
)

def setup() -> Typer:
    """
    Register configuration-related commands.
    """

    config_app = Typer(name="config", help="Manage rune configs. Run `rune config -h` for more help.")

    @config_app.command(name="storage")
    def config_storage(
        _mode: Annotated[
        Optional[Literal["local"]],
        Option("--mode", "-m", help=STORAGE_MODE_HELP),
    ] = None,
        _file: Annotated[
        Optional[str],
        Option("--file", "-f", help=STORAGE_FILE_HELP),
    ] = None,
    ):
        """
        Configure how and where secrets are stored.
        """
        context = Context.get()
        mode: str = _mode or context.settings.storage.mode

        if mode == "local":
            file = require(_file, "A file path is required when using local storage.")
            path = Path(file)
            storage_path = str(path.expanduser().absolute())

            new_settings = FileBasedStorageSettings(storage_path)
            context.settings.update(storage=new_settings)

            display.success_panel(f"Storage file set to: [bold cyan]{storage_path}[/]\n[dim]Existing secrets were not modified.[/]", title="Storage Updated")

    @config_app.command(name="encryption")
    def config_encryption(
        mode: Annotated[
        Literal["aesgcm"],
        Option("--mode", "-m", help=ENCRYPTION_MODE_HELP),
    ],
    ):
        """
        Configure the encryption algorithm used by rune.
        """
        context = Context.get()

        if mode == context.settings.encryption.mode:
            display.failed_panel(f"Encryption mode is already set to '[bold]{mode}[/]'.", title="Nothing changed")
            return

        new_settings = EncryptionSettings.from_mode(mode)
        context.settings.update(encryption=new_settings)

        display.success_panel(f"Encryption mode set to '[bold]{mode}[/]'.\n\n" +\
            "[dim]Existing secrets remain encrypted with their original settings.[/]", title="Encryption Updated")

    @config_app.command(name="session")
    def config_session(
        _port: Annotated[int, Option("--port", "-p", help="The port for the local session daemon.")],
        _default_ttl: Annotated[Optional[int], Option("--default-ttl", "-ttl", help="The default ttl for the provided default key.")] = None,
    ):
        """
        Configure the session daemon used by rune.
        """
        context = Context.get()

        new_settings = DaemonSessionSettings(
            port=_port,
            _default_ttl=_default_ttl or context.settings.session.default_ttl,
        )
        context.settings.update(session=new_settings)

        display.success_panel(f"Session daemon port set to '[bold]{_port}[/]'.", title="Encryption Updated")



    @config_app.command(name="show")
    def show_config(
        profile: Annotated[
        Optional[str],
        Argument(
            help=(
                "Profile name to display.\n"
                    "If omitted, shows the currently active configuration."
            )
        ),
    ] = None,
    ):
        """
        Display the current configuration or a specific profile.
        """
        context = Context.get()

        if not profile:
            settings_file = context.settings_manager.settings_file
            settings = context.settings.to_dict()

            display.print("[bold]Active configuration:[/]")
            display.print(f"Settings file: [cyan]{settings_file}[/]")
            display.print_dict(settings)
            return

        settings = context.settings_manager.get_profile(profile)

        if not settings:
            display.failed_panel(f"Profile '[bold cyan]{profile}[/]' does not exist.")
            return

        display.print(f"[bold]Configuration for profile '[cyan]{profile}[/]':[/]")
        display.print_dict(settings.to_dict())

    @config_app.command(name="where")
    def whereis(
        interactive: Annotated[
        bool,
        Option(
            "--interactive",
            "-i",
            help="Interactively select a file path to copy to clipboard.",
        ),
    ] = False
    ):
        """
        Show where rune stores its configuration and profile files.
        """
        context = Context.get()
        settings_file = str(context.settings_manager.settings_file.absolute())
        profiles_file = str(context.settings_manager.profiles_file.absolute())

        if not interactive:
            display.panel(f"[bold]Settings file[/]: [cyan]{settings_file}[/]\n[bold]Profiles file[/]: [cyan]{profiles_file}[/]")
            return

        choices = [settings_file, profiles_file]

        display.panel(
            f"[bold cyan][1][/] Settings file: {settings_file}\n"
                f"[bold cyan][2][/] Profiles file: {profiles_file}",
            title="File Locations",
        )

        choice = get_choice_by_idx("Copy file path", choices)
        if choice:
            pyperclip.copy(choice)
            display.print("[green]Path copied to clipboard.[/]")

    return config_app

