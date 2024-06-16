from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


def load_key(path):
    with open(path,'r') as keyfile:
        codedkey = keyfile.read()
        key=base64.b64decode(codedkey)
    return key

# function to generate another key (if needed)
def generate_key():
    key=os.urandom(32)
    return key

def save_key(key, filename):
    with open(filename, 'w') as file:
        encoded_key = base64.b64encode(key).decode('utf-8')
        file.write(encoded_key)

def encrypt_aes(key, plaintext):
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, ciphertext

def decrypt_aes(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_text.decode()
