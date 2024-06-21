import mysql.connector


class DatabaseManager:
    def __init__(self, creds_path='DB/DB_creds.txt'):
        self.creds_path = creds_path
        self.creds = self.read_db_creds()

    def read_db_creds(self):
        creds = {}
        try:
            with open(self.creds_path, 'r') as f:
                for line in f:
                    name, value = line.strip().split('=')
                    creds[name] = value
        except FileNotFoundError:
            print("Error: The 'DB_creds.txt' file was not found.")
            exit(1)
        return creds

    def create_database(self):
        try:
            conn = mysql.connector.connect(
                user=self.creds["user"],
                password=self.creds["password"],
                host=self.creds["host"]
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.creds['database']}")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def create_table(self):
        try:
            conn = mysql.connector.connect(
                user=self.creds["user"],
                password=self.creds["password"],
                host=self.creds["host"],
                database=self.creds["database"]
            )
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255),
                password VARCHAR(255),
                iv VARCHAR(255)
            )
            """)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def delete_table(self):
        try:
            conn = mysql.connector.connect(
                user=self.creds['user'],
                password=self.creds['password'],
                host=self.creds['host'],
                database=self.creds['database']
            )
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS Passwords")
            cursor.close()
            conn.close()
            print("Table 'Passwords' deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def insert_password(self, website, password, iv):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO Passwords (website, password, iv) VALUES (%s, %s, %s)"
            val = (website, password, iv)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_passwords(self, website):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT iv, password FROM Passwords WHERE website = %s", (website,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            passwords = []
            for row in rows:
                iv_from_db, ciphertext_from_db = bytes.fromhex(row[0]), bytes.fromhex(row[1])
                passwords.append((iv_from_db, ciphertext_from_db))

            return passwords
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def delete_password(self, website):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM Passwords WHERE website = %s"
            cursor.execute(sql, (website,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def get_connection(self):
        return mysql.connector.connect(
            user=self.creds["user"],
            password=self.creds["password"],
            host=self.creds["host"],
            database=self.creds["database"]
        )
