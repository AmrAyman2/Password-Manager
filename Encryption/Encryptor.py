from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


def generate_key():
    key = os.urandom(32)
    return key


class Encryptor:
    def __init__(self, key_path):
        self.key_path = key_path
        self.key = self.check_key()

    def load_key(self):
        with open(self.key_path, 'r') as keyfile:
            coded_key = keyfile.read()
            key = base64.b64decode(coded_key)
        return key

    # function to generate another key (if needed)

    def save_key(self):
        with open(self.key_path, 'w') as file:
            encoded_key = base64.b64encode(self.key).decode('utf-8')
            file.write(encoded_key)

    def check_key(self):
        with open(self.key_path, "r") as file:
            first_char = file.read(1)

            if not first_char:
                self.key = generate_key()
                self.save_key()
                return self.key
            else:
                return self.load_key()

    def encrypt_aes(self, plaintext):
        iv = os.urandom(16)  # Generate a random 16-byte IV
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return iv, ciphertext

    def decrypt_aes(self, iv, ciphertext):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text.decode()

    def decrypt_and_display_password(self, record_id, password_record):
        iv_from_db = password_record[2]
        ciphertext_from_db = password_record[3]
        iv_bytes = bytes.fromhex(iv_from_db)
        ciphertext_bytes = bytes.fromhex(ciphertext_from_db)
        decrypted_password = self.decrypt_aes(iv_bytes, ciphertext_bytes)
        print(f"Record: ID={record_id}, Username={password_record[1]}, Password (decrypted): {decrypted_password}")
        return decrypted_password
