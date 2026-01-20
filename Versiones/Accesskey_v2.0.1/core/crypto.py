# core/crypto.py
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

class CryptoManager:
    def __init__(self, password: str, salt: bytes):
        self.key = self._derive_key(password, salt)
        self.fernet = Fernet(self.key)

    def _derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )
        return base64.urlsafe_b64encode(
            kdf.derive(password.encode())
        )

    def encrypt(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)
