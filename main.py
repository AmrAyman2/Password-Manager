import sys
from DB.DatabaseManager import DatabaseManager
from Encryption.Encryptor import Encryptor
from PasswordManager import PasswordManager


def exit_program():
    print("Exiting...")
    sys.exit()


def main():
    path = "key.txt"
    dbmanager = DatabaseManager()
    encryptor = Encryptor(path)
    passmanager = PasswordManager(dbmanager, encryptor)

    dbmanager.create_database()  # Ensure database is created
    dbmanager.create_table()  # Ensure table is created
    encryptor.check_key()

    actions = {
        '1': passmanager.store_password,
        '2': passmanager.fetch_passwords_and_decrypt,
        '3': passmanager.delete_password_record,
        '4': exit_program,
        '99': dbmanager.delete_table
    }

    while True:
        print(
            "What would you like to do? \n 1) Store a Password \n 2) Fetch a password \n 3) Delete a password record "
            "\n 4) Exit")
        choice = input("Input: ")

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
