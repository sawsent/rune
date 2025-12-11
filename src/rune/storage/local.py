from typing import Dict, Optional, List
from rune.exception.notfounderror import NotFoundError
from rune.models.secret import Secret
from rune.storage.base import StorageManager
from json import load, dump

class LocalJsonStorageManager(StorageManager):

    def __init__(self, secrets_file_path: str) -> None:
        self.__secrets_file_path = secrets_file_path

    def full_name(self, name: str, namespace: str) -> str:
        if namespace == "":
            return name
        return namespace + "/" + name

    def store_secret(self, secret: Secret) -> bool:
        """
        Stores the provided ciphertext under the provided secret name.

        Returns True if storage is successful, False otherwise.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name()
        secrets[secret.full_name] = secret

        return self.store_secrets(secrets)

    def retreive_secret(self, name: str, namespace: str) -> Optional[Secret]:
        """
        Retreives the provided ciphertext under the provided secret name.

        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name()
        return secrets.get(self.full_name(name, namespace))

    def delete_secret(self, name: str, namespace: str) -> bool:
        """
        Deletes the entry with the provided name.

        Returns True if successful, False if it fails.
        Raises NotFoundError if it fails to find a secrets file.
        """
        secrets = self.stored_secrets_by_full_name()
        full_name = self.full_name(name, namespace)
        if not full_name in secrets:
            return False
        
        removed = {n: s for n, s in secrets.items() if not n == full_name}

        return self.store_secrets(removed)


    def get_all_secrets(self) -> List[Secret]:
        """
        Retrieves all entry names.

        Raises NotFoundError if it fails to retreive entries.
        """
        try:
            with open(self.__secrets_file_path, "r") as f:
                d = load(f)
                return [ Secret.from_dict(v) for _, v in d.items() ]
        except:
            raise NotFoundError(f"Secrets file at {self.__secrets_file_path} not found")


    def store_secrets(self, secrets: Dict[str, Secret]) -> bool:
        try:
            with open(self.__secrets_file_path, "w") as f:
                to_dump = {s.id: s.to_dict() for s in secrets.values()}
                dump(to_dump, f, indent=4)
                return True
        except:
            return False


    def stored_secrets_by_full_name(self) -> Dict[str, Secret]:
        secrets = self.get_all_secrets()
        return {s.full_name: s for s in secrets}
        


