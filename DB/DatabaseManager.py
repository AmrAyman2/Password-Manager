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
                username VARCHAR(255),
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
            input("Press any key to exit...")
            exit(1)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def insert_password(self, website, username, password, iv):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO Passwords (website, username, password, iv) VALUES (%s, %s, %s, %s)"
            val = (website, username, password, iv)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def fetch_passwords(self, website):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "SELECT id, username, iv, password FROM Passwords WHERE website = %s"
            cursor.execute(sql, (website,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def fetch_single_password(self,website,username):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "SELECT id, password, iv FROM Passwords WHERE website = %s AND username = %s"
            cursor.execute(sql, (website, username))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result  # Returns (id, ciphertext, iv) if record exists, else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def update_password(self, record_id, ciphertext, iv):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "UPDATE Passwords SET password = %s, iv = %s WHERE id = %s"
            cursor.execute(sql, (ciphertext, iv, record_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def delete_password(self, record_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM Passwords WHERE id = %s"
            cursor.execute(sql, (record_id,))
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
