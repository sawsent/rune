from typer import Argument, Typer, Option
from typing import Annotated
import typer

from rune.context import Context
from rune.utils.input import get_choice_by_idx
from rune.utils import display

def setup() -> Typer:
    profile_app = Typer(name="profile", help="Manage configuration profiles. `rune config profile -h` for more help.")

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

    return profile_app

