import sys
from DB.sql import delete_password, fetch_passwords, get_connection, insert_password
from Encryption.aes import decrypt_aes, encrypt_aes, load_key

global key
path ="key.txt" # write the path to the file that contains your key
key=load_key(path)

def exit_program():
    print("Exiting...")
    sys.exit()

def store_password():
    website = input("Enter the website: ")
    plaintext_password = input("Enter the password: ")
    iv, ciphertext = encrypt_aes(key, plaintext_password)
    conn = get_connection()
    insert_password(conn, website, ciphertext.hex(), iv.hex())
    conn.close()
    print("Password stored successfully.")

def fetch_passwords_and_decrypt():
    website = input("Enter the website to fetch passwords for: ")
    conn = get_connection()
    passwords = fetch_passwords(conn, website)
    conn.close()

    if passwords:
        for index, (iv_from_db, ciphertext_from_db) in enumerate(passwords, start=1):
            decrypted_password = decrypt_aes(key, iv_from_db, ciphertext_from_db)
            print(f"Password {index}: {decrypted_password}")
    else:
        print(f"No passwords found for {website}.")

def delete_password_record():
    website = input("Enter the website to delete the password record for: ")
    conn = get_connection()
    deleted = delete_password(conn, website)
    conn.close()
    if deleted:
        print(f"Deleted password record for {website}.")
    else:
        print(f"No password record found for {website}.")

def exit_program():
    print("Exiting...")
    sys.exit()