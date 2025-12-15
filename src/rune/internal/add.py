from rune.context import Context
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.models.crypto.secret import Secret

from typing import Dict


def add_secret(user: str, full_name: str, fields: Dict[str, str], key: str) -> Result[None]:
    """
    Encrypts a secret with the configured encrypter.
    Stores the encrypted secret with the configured storage manager.

    Returns the result.
    """
    encrypter = Context.get().configured_encrypter
    storage = Context.get().storage_manager

    encrypted_fields = {name: encrypter.encrypt(secret, key) for name, secret in fields.items()}

    model = Secret(
        full_name = full_name,
        user = user,
        algorithm = encrypter._encryption_algorithm,
        fields = encrypted_fields
    )

    fqn = model.full_name

    try:
        if storage.retreive_secret(user, fqn) is not None:
            return Failure(f"Secret '{fqn}' already exists. You can update it with `rune update -n {fqn}`")

        return Success() if storage.store_secret(model) else Failure(f"Storage manager could not store the secret {fqn}")


    except NotFoundError as err:
        return Failure(err.message)

