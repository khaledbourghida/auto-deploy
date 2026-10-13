import keyring
from cryptography.fernet import Fernet

class Security:
    SERVICE_NAME = "auto_deploy_app"
    KEY_NAME = "encryption_key"

    def __init__(self):
        key_str = self.get_or_create_encryption_key()
        self._fernet = Fernet(key_str.encode())

    def get_or_create_encryption_key(self) -> str:
        key = keyring.get_password(self.SERVICE_NAME, self.KEY_NAME)

        if key is None:
            key = Fernet.generate_key().decode()
            keyring.set_password(self.SERVICE_NAME, self.KEY_NAME, key)

        return key

    def encrypt_token(self, token: str) -> str:
        return self._fernet.encrypt(token.encode()).decode()

    def decrypt_token(self, encrypted_token: str) -> str:
        return self._fernet.decrypt(encrypted_token.encode()).decode()
