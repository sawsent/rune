from rune.utils.settings import get_configured_storage_manager_identifier


def get_configured_storage_manager():
    manager_identifier = get_configured_storage_manager_identifier()
    match manager_identifier:
        case "local":
            from rune.storage.local import LocalStorageManager
            return LocalStorageManager()
        case _:
            from rune.storage.local import LocalStorageManager
            return LocalStorageManager()
