from rune.encryption import factory as EncryptionFactory
from rune.exception.notfounderror import NotFoundError
from rune.models.result import Failure, Result, Success
from rune.models.secret import Secret
from rune.storage import factory as StorageManagerFactory
from typing import Dict

def add_secret(name: str, fields: Dict[str, str], key: str, namespace: str = "") -> Result[None]:
    """
    Encrypts a secret with the configured encrypter.
    Stores the encrypted secret with the configured storage manager.

    Returns the result.
    """
    encrypter = EncryptionFactory.get_configured_encrypter()
    storage = StorageManagerFactory.get_configured_storage_manager()

    encrypted_fields = {name: encrypter.encrypt(secret, key) for name, secret in fields.items()}

    model = Secret(
        name = name,
        namespace = namespace,
        algorithm = encrypter._encryption_algorithm,
        fields = encrypted_fields
    )

    try:
        if storage.retreive_ciphertext(name, namespace) is not None:
            return Failure(f"Secret '{name}' already exists. You can update it with `rune update -n {name}`")

        if storage.store_ciphertext(model):
            return Success()
        else:
            return Failure(f"Storage manager could not store the secret {name}")

    except NotFoundError as err:
        return Failure(err.message)

