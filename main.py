from DB.sql import create_database, delete_table, create_table
from program import delete_password_record, fetch_passwords_and_decrypt, store_password,exit_program


def main():
    create_database()  # Ensure database is created
    create_table()     # Ensure table is created

    actions = {
        '1': store_password,
        '2': fetch_passwords_and_decrypt,
        '3': delete_password_record,
        '4': exit_program,
        '99': delete_table  
    }

    while True:
        print("What would you like to do? \n 1) Store a Password \n 2) Fetch a password \n 3) Delete a password record \n 4) Exit")
        choice = input("Input: ")

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()