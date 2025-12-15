from typing import Dict, Optional, List
from rune.models.crypto.secret import Secret
from rune.storage.secrets.base import StorageManager
from json import load, dump
import os

class LocalJsonStorageManager(StorageManager):
    def __init__(self, secrets_file_path: str) -> None:
        self.__secrets_file_path = secrets_file_path
        self._ensure_secrets()

    def _ensure_secrets(self) -> None:
        if not os.path.exists(self.__secrets_file_path):
            with open(self.__secrets_file_path, "w") as f:
                dump({}, f, indent=4)

    def store_secret(self, secret: Secret) -> bool:
        """
        Stores the provided ciphertext under the provided secret name.

        Returns True if storage is successful, False otherwise.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name(secret.user)
        secrets[secret.full_name] = secret

        return self.store_secrets(secrets)

    def retreive_secret(self, user: str, name: str) -> Optional[Secret]:
        """
        Retreives the provided ciphertext under the provided secret name.

        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name(user)
        return secrets.get(name)

    def delete_secret(self, user: str, name: str) -> bool:
        """
        Deletes the entry with the provided name.

        Returns True if successful, False if it fails.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name(user)
        if not name in secrets:
            return False
        
        removed = {n: s for n, s in secrets.items() if not n == name}

        return self.store_secrets(removed)


    def get_all_secrets(self, user: str) -> List[Secret]:
        """
        Retrieves all entry names.
        """
        with open(self.__secrets_file_path, "r") as f:
            d = load(f)
            all_secrets = [ Secret.from_dict(v) for _, v in d.items() ]
            return [s for s in all_secrets if s.user == user]


    def store_secrets(self, secrets: Dict[str, Secret]) -> bool:
        try:
            with open(self.__secrets_file_path, "w") as f:
                to_dump = {s.id: s.to_dict() for s in secrets.values()}
                dump(to_dump, f, indent=4)
                return True
        except:
            return False


    def stored_secrets_by_full_name(self, user: str) -> Dict[str, Secret]:
        secrets = self.get_all_secrets(user)
        return {s.full_name: s for s in secrets}
        


