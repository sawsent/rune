from typing import Dict, Optional, List
from rune.exception.notfounderror import NotFoundError
from rune.models.secret import Secret
from rune.storage.base import StorageManager
from json import load, dump

class LocalJsonStorageManager(StorageManager):

    def __init__(self, secrets_file_path: str) -> None:
        self.__secrets_file_path = secrets_file_path

    def full_name(self, name: str, namespace: str) -> str:
        return namespace + "/" + name

    def store_ciphertext(self, secret: Secret) -> bool:
        """
        Stores the provided ciphertext under the provided secret name.

        Returns True if storage is successful, False otherwise.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.get_stored_secrets()
        secrets[secret.full_name] = secret

        return self.store_secrets(secrets)

    def retreive_ciphertext(self, name: str, namespace: str = "") -> Optional[Secret]:
        """
        Retreives the provided ciphertext under the provided secret name.

        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.get_stored_secrets()
        return secrets.get(self.full_name(name, namespace))

    def delete_entry(self, name: str, namespace: str = "") -> bool:
        """
        Deletes the entry with the provided name.

        Returns True if successful, False if it fails.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.get_stored_secrets()
        full_name = self.full_name(name, namespace)
        if not full_name in secrets:
            return False
        
        removed = {n: s for n, s in secrets.items() if not n == full_name}

        return self.store_secrets(removed)


    def get_entries(self) -> List[Secret]:
        """
        Retrieves all entry names.

        Raises NotFoundError if it fails to retreive entries.
        """
        secrets = self.get_stored_secrets()
        return list(secrets.values())

    def store_secrets(self, secrets: Dict[str, Secret]) -> bool:
        try:
            with open(self.__secrets_file_path, "w") as f:
                to_dump = {k: v.to_dict() for k, v in secrets.items()}
                dump(to_dump, f, indent=4)
                return True
        except:
            return False


    def get_stored_secrets(self) -> Dict[str, Secret]:
        try:
            with open(self.__secrets_file_path, "r") as f:
                d = load(f)
                return { k: Secret.from_dict(v) for k, v in d.items() }
        except:
            raise NotFoundError(f"Secrets file at {self.__secrets_file_path} not found")



