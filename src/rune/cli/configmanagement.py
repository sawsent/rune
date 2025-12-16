from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.prompt import Prompt
from typer import Argument, Typer, Option
from typing import Annotated, Literal, Optional

from rune.context import Context
from rune.models.settings.encryptionsettings import EncryptionSettings
from rune.models.settings.storagesettings import FileBasedStorageSettings
from rune.utils.input import get_int_or_quit, require

STORAGE_MODE_HELP = "Configure how and where rune stores encrypted secrets."
STORAGE_FILE_HELP = "Where to store secrets (file) if storage mode is 'local'"

ENCRYPTION_MODE_HELP = "Configure how and where rune stores encrypted secrets."

console = Console()

def setup(app: Typer):

    profile_app = Typer(name="profile", help="Manage config profiles.")
    
    @profile_app.command(name="list")
    def list_profiles(
        interactive: Annotated[bool, Option("--interactive", "-i", help="Choose profile after displaying.")] = False
    ):
        """
        Show the list of configured profiles.
        """
        settings_manager = Context.get().settings_manager

        profiles = [k for k in settings_manager.get_profiles().keys()]
        profiles_file = str(settings_manager.profiles_file.absolute())
        
        console.print(f"Profiles at [bold cyan]{profiles_file}[/]")
        if not profiles:
            console.print(Panel.fit((
                "[yellow]No profiles configured yet.[/]\n"
                "You can create profiles with [bold cyan]`rune config profile save <profile name>`[/]")
            ))
            return

        console.print(Panel.fit(
            "\n".join([f"[bold cyan][{idx}][/] {profile}" for idx, profile in enumerate(profiles, 1)])
        ))

        if not interactive:
            return

        choice = get_int_or_quit("Choose profile to activate")

        if not choice:
            return

        use_profile(profiles[choice - 1])


    @profile_app.command(name="save")
    def save_profile(
        _name: Annotated[str, Argument(help="The name for the profile to be stored under")],
        _force: Annotated[bool, Option("--force", "-f", help="If `--force`, will override existing profile")] = False
    ):
        """
        Save the current settings to a profile.

        Will fail if profile already exists, or override it if `--force`.
        """
        context = Context.get()
        settings_manager = context.settings_manager

        if _name in settings_manager.get_profiles() and not _force:
            console.print(Panel.fit(
                f"Profile '[bold cyan]{_name}[/]' already exists. Use `rune config profile save {_name} --force` to override.",
                title="[red]Failed[/]"
            ))
            return

        settings_manager.save_profile(context.settings, _name)
        console.print(Panel.fit(
            f"Stored profile '[bold cyan]{_name}[/]' with the current settings",
            title="[green]Success[/]"
        ))
        return

    @profile_app.command(name="use")
    def use_profile(
        _name: Annotated[str, Argument(help="The name for the profile to be used.")],
    ):
        """
        Save the current settings to a profile.

        Will fail if profile already exists, or override it if `--force`.
        """
        context = Context.get()
        settings_manager = context.settings_manager

        settings = settings_manager.get_profile(_name)

        if not settings:
            console.print(Panel.fit(
                f"Profile '[bold cyan]{_name}[/]' does not exist.",
                title="[red]Failed[/]"
            ))
            return

        context.settings = settings.dirty()
        settings_manager.save_profile(settings, _name)
        console.print(Panel.fit(
            f"Switched to profile '[bold cyan]{_name}[/]'.",
            title="[green]Success[/]"
        ))
        return


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

    @app.command(name="show")
    def show_config(
        profile: Annotated[Optional[str], Argument(help="What configuration to show (which profile). If empty, will show the active settings.")] = None,
    ):
        """
        Display the rune config.
        """
        context = Context.get()

        if not profile:
            settings_file = context.settings_manager.settings_file
            settings = context.settings.to_dict()
            console.print(f"[bold]Displaying [cyan]active[/cyan] settings:[/]")
            console.print(f"Settings file located at: [bold cyan]'{settings_file}'[/].")
            console.print(Pretty(settings, expand_all=True, indent_guides=True))
            return
        
        settings = context.settings_manager.get_profile(profile)

        if not settings:
            console.print(Panel.fit(
                f"Profile '[bold cyan]{profile}[/]' does not exist.",
                title="[red]Failed[/]",
            ))
            return

        console.print(f"[bold]Displaying settings for profile '[cyan]{profile}[/cyan]':[/]")
        console.print(Pretty(settings, expand_all=True, indent_guides=True))

    app.add_typer(profile_app)



