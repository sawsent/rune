from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.storage import factory as StorageManagerFactory

def delete_secret(name: str, namespace: str = "") -> Result[None]:
    """
    Deletes the encrypted secret via the configured storage manager.

    Returns the reason for failure, if it fails.
    None if is successful.
    """
    storage = StorageManagerFactory.get_configured_storage_manager()

    try:
        if storage.retreive_secret(name, namespace) is None:
            return Failure(f"Secret '{name}' does not exist.")

        if storage.delete_secret(name, namespace):
            return Success()
        else:
            return Failure(f"Storage manager could not delete secret '{name}'")

    except NotFoundError as err:
        return Failure(err.message)

