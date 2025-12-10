from rune.storage.factory import get_configured_storage_manager

def list_secrets() -> None:
    storage = get_configured_storage_manager()
    entries = storage.get_entries()
    [print(e) for e in entries]

