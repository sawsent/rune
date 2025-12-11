from typing import List
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.models.secret import Secret
from rune.storage import factory as StorageManagerFactory

def list_secrets() -> Result[List[Secret]]:
    """
    Retrieves all secret entries with the configured storage manager.
    Returns None if it there is an error getting the secrets.
    """
    storage = StorageManagerFactory.get_configured_storage_manager()
    try:
        return Success(storage.get_all_secrets())
    except NotFoundError as err:
        return Failure(err.message)

