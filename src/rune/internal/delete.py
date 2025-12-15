from rune.context import Context
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success

def delete_secret(user: str, full_name: str) -> Result[None]:
    """
    Deletes the encrypted secret via the configured storage manager.

    Returns the reason for failure, if it fails.
    None if is successful.
    """
    storage = Context.get().storage_manager

    try:
        if storage.retreive_secret(user, full_name) is None:
            return Failure(f"Secret '{full_name}' does not exist.")

        if storage.delete_secret(user, full_name):
            return Success()
        else:
            return Failure(f"Storage manager could not delete secret '{full_name}'")

    except NotFoundError as err:
        return Failure(err.message)

