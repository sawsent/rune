import typer
from rune.context import Context
from rune.crypto.factory import get_encrypter_by_algorithm
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Failure, Result, Success

def delete_secret(user: str, full_name: str, hard: bool, key: str) -> Result[None]:
    """
    Deletes the encrypted secret via the configured storage manager.

    Returns the reason for failure, if it fails.
    None if is successful.
    """
    storage = Context.get().storage_manager

    secret = storage.retreive_secret(user, full_name)

    if not secret:
        return Failure(f"Secret '{full_name}' does not exist.")

    if not typer.confirm(f"Are you sure you want do delete secret '{full_name}'?"):
        raise typer.Abort()

    if not hard:
        return Success() if storage.delete_secret(user, full_name, hard=False) else Failure(f"Error deleting secret '{full_name}'")

    encrypter = get_encrypter_by_algorithm(secret.algorithm)

    try:
        [encrypter.decrypt(sf, key) for sf in secret.fields.values()]
        return Success() if storage.delete_secret(user, full_name, hard=True) else Failure(f"Error deleting secret '{full_name}'")

    except WrongKeyUsed as e:
        return Failure(e.message)

def restore_secret(user: str, full_name: str) -> Result[None]:
    storage = Context.get().storage_manager

    secret = storage.retreive_secret(user, full_name)

    if not secret:
        return Failure(f"Secret {full_name} does not exist. It might have been hard deleted.")
    
    if not secret.deleted:
        return Failure(f"Secret {full_name} is not deleted.")
    
    return Success() if storage.restore_secret(user, full_name) else Failure("Error restoring secret '{full_name}'")



