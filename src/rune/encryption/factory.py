from rune.encryption.base import Encrypter
from rune.utils.settings import get_configured_encryption_identifier

def get_configured_encrypter() -> Encrypter:
    encryption = get_configured_encryption_identifier()

    match encryption:
        case "no-encryption":
            from rune.encryption.noencryption import NoEncryption
            return NoEncryption()
        case _: 
            from rune.encryption.noencryption import NoEncryption
            return NoEncryption()
