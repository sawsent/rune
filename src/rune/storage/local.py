from typing import Dict, Optional, List
from rune.storage.base import StorageManager
from rune.utils.settings import get_secrets_path
from json import load, dump

class LocalStorageManager(StorageManager):
    def store_ciphertext(self, name: str, ciphertext: str) -> None:
        """
        Stores the provided ciphertext under the provided secret name.
        """
        secrets = self.__stored_secrets
        secrets[name] = ciphertext

        with open(get_secrets_path(), "w") as f:
            dump(secrets, f, indent=4)

    def retreive_ciphertext(self, name: str) -> Optional[str]:
        """
        Retreives the provided ciphertext under the provided secret name.
        """
        return self.__stored_secrets.get(name)

    def get_entries(self) -> List[str]:
        """
        Retrieves all entry names.
        """
        return list(self.__stored_secrets.keys())


    @property
    def __stored_secrets(self) -> Dict[str, str]:
        try:
            with open(get_secrets_path(), "r") as f:
                return load(f)
        except:
            return {}

