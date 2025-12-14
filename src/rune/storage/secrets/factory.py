from rune.utils.settings import get_configured_storage_manager_identifier, get_secrets_path
from rune.storage.secrets.local import LocalJsonStorageManager

def get_configured_storage_manager():
    manager_identifier = get_configured_storage_manager_identifier()
    match manager_identifier:
        case "local":
            return LocalJsonStorageManager(get_secrets_path())
        case _:
            raise ValueError(f"Storage manager does not exist for identifier {manager_identifier}.")
