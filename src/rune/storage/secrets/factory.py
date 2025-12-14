from rune.models.settings.settings import Settings
from rune.models.settings.storagesettings import FileBasedStorageSettings
from rune.storage.secrets.base import StorageManager
from rune.storage.secrets.local import LocalJsonStorageManager

def get_storage_manager(settings: Settings) -> StorageManager:
    match settings.storage:
        case FileBasedStorageSettings(file=file):
            return LocalJsonStorageManager(file)
        case _:
            raise ValueError(f"Storage manager does not exist for identifier {settings.storage.mode}.")


