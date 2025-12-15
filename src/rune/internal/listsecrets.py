from rune.context import Context
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.models.crypto.secret import Secret

from typing import List

def list_secrets(user: str) -> Result[List[Secret]]:
    """
    Retrieves all secret entries with the configured storage manager.
    Returns None if it there is an error getting the secrets.
    """
    storage = Context.get().storage_manager
    try:
        return Success(storage.get_all_secrets(user))
    except NotFoundError as err:
        return Failure(err.message)

