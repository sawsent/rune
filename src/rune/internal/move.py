from rune.context import Context
from rune.models.result import Failure, Result, Success


def move_secret(user: str, original_name: str, new_name: str) -> Result[None]:

    storage = Context.get().storage_manager

    secret = storage.retreive_secret(user, original_name)

    if secret is None:
        return Failure(f"Secret '{original_name}' does not exist")

    if storage.move_secret(user, original_name, new_name):
        return Success()
    else:
        return Failure(f"Unable to move secret '{original_name}'")


