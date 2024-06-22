class PasswordManager:
    def __init__(self, db_manager, encryptor):
        self.db_manager = db_manager
        self.encryptor = encryptor

    def store_password(self):
        website = input("Enter the website: ")
        username = input("Enter the username: ")
        plaintext_password = input("Enter the password: ")

        # Check if there's already a record with the same website and username
        existing_password = self.db_manager.fetch_single_password(website, username)
        if existing_password:
            if input("There's a record with that username do you want to update it? (Y/N) : ").lower() == "y":
                # If record exists, update it
                iv, password = self.encryptor.encrypt_aes(plaintext_password)
                if self.db_manager.update_password(existing_password[0], password.hex(), iv.hex()):
                    print(f"Password updated successfully for {website} and username {username}.")
                else:
                    print(f"Failed to update password for {website} and username {username}.")
            else:
                print("Storing new password aborted")
                return
        else:
            # If no record exists, insert a new password
            iv, password = self.encryptor.encrypt_aes(plaintext_password)
            if self.db_manager.insert_password(website, username, password.hex(), iv.hex()):
                print("Password stored successfully.")
            else:
                print("Failed to store the password.")

    def fetch_passwords_and_decrypt(self):
        website = input("Enter the website to fetch passwords for: ")
        passwords = self.db_manager.fetch_passwords(website)

        if passwords:
            for index, (record_id, username, iv_from_db, ciphertext_from_db) in enumerate(passwords, start=1):
                iv_bytes = bytes.fromhex(iv_from_db)
                ciphertext_bytes = bytes.fromhex(ciphertext_from_db)
                decrypted_password = self.encryptor.decrypt_aes(iv_bytes, ciphertext_bytes)
                print(f"Password {index}: Username : {username}, Password : {decrypted_password}")
        else:
            print(f"No passwords found for {website}.")

    def delete_password_record(self):
        website = input("Enter the website to delete the password record for: ")
        passwords = self.db_manager.fetch_passwords(website)

        if not passwords:
            print(f"No password records found for {website}.")
            return

        if len(passwords) == 1:
            # If there's only one record, delete it directly
            record_id = passwords[0][0]
            decrypted_password = self.encryptor.decrypt_and_display_password(record_id, passwords[0])
            if decrypted_password:
                if self.db_manager.delete_password(record_id):
                    print(f"Deleted password record for {website}.")
                else:
                    print(f"Failed to delete password record for {website}.")
        else:
            # If there are multiple records, ask the user which one to delete
            print("Multiple records found:")
            for index, (record_id, username, iv_from_db, ciphertext_from_db) in enumerate(passwords, start=1):
                iv_bytes = bytes.fromhex(iv_from_db)
                ciphertext_bytes = bytes.fromhex(ciphertext_from_db)
                decrypted_password = self.encryptor.decrypt_aes(iv_bytes, ciphertext_bytes)
                print(f"{index}: ID : {record_id}, Username : {username}, Password : {decrypted_password}")

            choice = int(input("Enter the number of the record to delete: "))
            if 1 <= choice <= len(passwords):
                record_id = passwords[choice - 1][0]
                if self.db_manager.delete_password(record_id):
                    print(f"Deleted password record with ID {record_id} for {website}.")
                else:
                    print(f"Failed to delete password record with ID {record_id} for {website}.")
            else:
                print("Invalid choice. No record deleted.")
