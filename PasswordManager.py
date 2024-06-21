import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class PasswordManager:
    def __init__(self, db_manager, encryptor):
        self.db_manager = db_manager
        self.encryptor = encryptor

    def store_password(self):
        website = input("Enter the website: ")
        plaintext_password = input("Enter the password: ")
        iv, ciphertext = self.encryptor.encrypt_aes(plaintext_password)
        self.db_manager.insert_password(website, ciphertext.hex(), iv.hex())
        print("Password stored successfully.")

    def fetch_passwords_and_decrypt(self):
        website = input("Enter the website to fetch passwords for: ")
        passwords = self.db_manager.fetch_passwords(website)

        if passwords:
            for index, (iv_from_db, ciphertext_from_db) in enumerate(passwords, start=1):
                decrypted_password = self.encryptor.decrypt_aes(iv_from_db, ciphertext_from_db)
                print(f"Password {index}: {decrypted_password}")
        else:
            print(f"No passwords found for {website}.")

    def delete_password_record(self):
        website = input("Enter the website to delete the password record for: ")
        deleted = self.db_manager.delete_password(website)
        if deleted:
            print(f"Deleted password record for {website}.")
        else:
            print(f"No password record found for {website}.")