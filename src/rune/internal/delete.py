from rune.context import Context
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.utils.input import get_fqn

def delete_secret(user: str, name: str, namespace: str) -> Result[None]:
    """
    Deletes the encrypted secret via the configured storage manager.

    Returns the reason for failure, if it fails.
    None if is successful.
    """
    storage = Context.get().storage_manager

    fqn = get_fqn(name, namespace)

    try:
        if storage.retreive_secret(user, fqn) is None:
            return Failure(f"Secret '{fqn}' does not exist.")

        if storage.delete_secret(user, fqn):
            return Success()
        else:
            return Failure(f"Storage manager could not delete secret '{fqn}'")

    except NotFoundError as err:
        return Failure(err.message)

