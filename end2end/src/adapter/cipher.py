import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from src.infra.cipher import BaseCipher

class Cipher(BaseCipher):

    def __init__(self):
        secret_key = os.getenv('CIPHER_KEY')
        if secret_key is None or secret_key == "":
            raise Exception('Cipher key not config')
        
        self.fernet = Fernet(secret_key)
        self.digest = hashes.Hash(hashes.SHA256())
    
    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()
    
    def hash(self, data: str) -> str:
        self.digest.update(data.encode())
        return self.digest.finalize().hex()
