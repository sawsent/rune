from rune.models.settings.sessionsettings import DaemonSessionSettings, SessionSettings
from rune.models.settings.settings import Settings
from rune.session.base import SessionManager
from rune.session.daemonmgr import DaemonSessionManager


def get_session_manager(settings: Settings) -> SessionManager:
    session_settings = settings.session
    match session_settings.mode:
        case SessionSettings.DAEMON if isinstance(session_settings, DaemonSessionSettings):
            return DaemonSessionManager("localhost", session_settings.port)
        case _:
            raise ValueError(f"Unexpected session mode: {session_settings.mode}")

