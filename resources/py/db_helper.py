import mysql.connector
from mysql.connector import Error


class DBHelper:
    def __init__(self, host, user, password, database):

        try:
            self.connection = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            if self.connection.is_connected():
                print("Connected to the database.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    # read records from given table
    def read(self, table):
        query = f"SELECT * FROM {table};"
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            records = cursor.fetchall()  # List of dictionaries
            return records

        except Error as e:
            print(f"Error reading records: {e}")
            return []
        finally:
            cursor.close()

    def close_connection(self):
        """Close the database connection if open."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
