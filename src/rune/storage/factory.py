from rune.utils.settings import get_configured_storage_manager_identifier, get_secrets_path


def get_configured_storage_manager():
    manager_identifier = get_configured_storage_manager_identifier()
    match manager_identifier:
        case "local":
            from rune.storage.local import LocalJsonStorageManager
            return LocalJsonStorageManager(get_secrets_path())
        case _:
            from rune.storage.local import LocalJsonStorageManager
            return LocalJsonStorageManager(get_secrets_path())
