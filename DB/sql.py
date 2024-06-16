import mysql.connector

# Get credentials from the txt file
def read_DB_creds():
    creds = {}
    try:
        with open('DB//DB_creds.txt', 'r') as f:
            for line in f:
                name, value = line.strip().split('=')
                creds[name] = value
    except FileNotFoundError:
        print("Error: The 'DB_creds.txt' file was not found.")
        exit(1)
    return creds

# Connect to MySQL server and create database if it doesn't exist
def create_database():
    creds = read_DB_creds()
    try:
        conn = mysql.connector.connect(
            user=creds["user"],
            password=creds["password"],
            host=creds["host"]
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {creds["database"]}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

# Create table if it doesn't exist
def create_table():
    creds= read_DB_creds()
    try:
        conn = mysql.connector.connect(
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            database=creds["database"]
        )
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            website VARCHAR(255),
            password VARCHAR(255),
            IV VARCHAR(255)
        )
        """)
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def delete_table():
    try:
        creds = read_DB_creds()
        conn = mysql.connector.connect(
            user=creds['user'],
            password=creds['password'],
            host=creds['host'],
            database=creds['database']
        )
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Passwords")
        cursor.close()
        conn.close()
        print("Table 'Passwords' deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def insert_password(conn, website, password, IV):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Passwords (Website, Password, IV) VALUES (%s, %s, %s)"
        val = (website, password, IV)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def fetch_passwords(conn, website):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT IV, Password FROM Passwords WHERE Website = %s", (website,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            iv_from_db, ciphertext_from_db = bytes.fromhex(row[0]), bytes.fromhex(row[1])
            return iv_from_db, ciphertext_from_db
        else:
            return None, None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def delete_password(conn, website):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Passwords WHERE Website = %s"
        cursor.execute(sql, (website,))
        conn.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def get_connection():
    creds = read_DB_creds()
    return mysql.connector.connect(
        user=creds["user"],
        password=creds["password"],
        host=creds["host"],
        database=creds["database"]
    )
