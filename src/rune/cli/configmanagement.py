from pathlib import Path
from typer import Argument, Typer, Option
from typing import Annotated, Literal, Optional
import pyperclip
import typer

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

def setup(app: Typer):
    """
    Register configuration-related commands.
    """

    profile_app = Typer(
        name="profile",
        help="Manage configuration profiles (save, switch, list, delete).",
    )

    @profile_app.command(name="list")
    def list_profiles(
        interactive: Annotated[
            bool,
            Option(
                "--interactive",
                "-i",
                help="Interactively select a profile to activate after listing.",
            ),
        ] = False
    ):
        """
        List all configured profiles.
        """
        settings_manager = Context.get().settings_manager

        profiles = list(settings_manager.get_profiles().keys())
        profiles_file = str(settings_manager.profiles_file.absolute())

        display.print(f"[bold]Profiles file:[/] [cyan]{profiles_file}[/]")

        if not profiles:
            display.panel("[yellow]No profiles configured yet.[/] Create one with:\n[bold cyan]rune config profile save <profile-name>[/]")
            return

        display.success_panel("\n".join(f"[bold cyan][{idx}][/] {profile}" for idx, profile in enumerate(profiles, 1)), title="Available Profiles")

        if not interactive:
            return

        choice = get_choice_by_idx("Select profile to activate", profiles)
        if not choice:
            return

        load_profile(choice)

    @profile_app.command(name="save")
    def save_profile(
        _name: Annotated[
        str, Argument(help="Name under which the current configuration will be saved.")
    ],
        _force: Annotated[
        bool,
        Option(
            "--force",
            "-f",
            help="Overwrite the profile if it already exists.",
        ),
    ] = False,
    ):
        """
        Save the current configuration as a profile.
        """
        context = Context.get()
        settings_manager = context.settings_manager

        if _name in settings_manager.get_profiles() and not _force:
            display.failed_panel(f"Profile '[bold cyan]{_name}[/]' already exists.\n\nUse [bold cyan]--force[/] to overwrite it.")
            return

        settings_manager.save_profile(context.settings, _name)
        display.success_panel(f"Profile '[bold cyan]{_name}[/]' saved successfully.")

    @profile_app.command(name="load")
    def load_profile(
        _name: Annotated[
        str, Argument(help="Name of the profile to activate.")
    ],
    ):
        """
        Activate a saved configuration profile.
        """
        context = Context.get()
        settings_manager = context.settings_manager

        settings = settings_manager.get_profile(_name)
        if not settings:
            display.failed_panel(f"Profile '[bold cyan]{_name}[/]' does not exist.")
            return

        context.settings = settings.dirty()
        settings_manager.save_profile(settings, _name)

        display.success_panel(f"Switched to profile '[bold cyan]{_name}[/]'.")

    @profile_app.command(name="delete")
    def delete_profile(
        _name: Annotated[
        str, Argument(help="Name of the profile to delete.")
    ],
    ):
        """
        Delete an existing profile.
        """
        context = Context.get()
        settings_manager = context.settings_manager

        profile = settings_manager.get_profile(_name)
        if not profile:
            display.failed_panel(f"Profile '[bold cyan]{_name}[/]' does not exist.")
            return

        if typer.confirm(f"Are you sure you want to delete profile '{_name}'?"):
            settings_manager.delete_profile(_name)
            display.success_panel(f"Profile '[bold cyan]{_name}[/]' deleted.")

        else:
            raise typer.Abort()

    @app.command(name="storage")
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

    @app.command(name="encryption")
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

    @app.command(name="session")
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



    @app.command(name="show")
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

    @app.command(name="where")
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

    app.add_typer(profile_app)

