import mysql.connector
from mysql.connector import Error
import re


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

    def get_columns_data(self, table):

        def process_columns_data(table_name, records, num_columns=3):
            # process returned data
            columns_data = {}

            for record in records:
                column_name = record["Field"]
                key_type = record["Key"]

                # grab type
                # # # # # # # # # # # # # # # # # # # # # # #
                column_type = record["Type"]

                # try to find the length (eg VARCHAR(255))
                match = re.search(r"\((\d+)\)", column_type)
                if match:
                    # if length is found remove it
                    column_type = column_type.split("(")[0]

                # grab fks
                # # # # # # # # # # # # # # # # # # # # # # #
                fks = self.run_query(
                    f"SELECT REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table_name}' AND  COLUMN_NAME = '{column_name}' AND REFERENCED_TABLE_NAME IS NOT NULL; "
                )

                fk_data = {}
                for fk in fks:
                    # grab sample data for foreign key, ensuring that the referenced column is included first
                    fk_list = self.run_query(
                        f"SELECT {fk['REFERENCED_COLUMN_NAME']}, {fk['REFERENCED_TABLE_NAME']}.* FROM {fk['REFERENCED_TABLE_NAME']};"
                    )

                    # simplify and use only the first two columns
                    fk_list = [
                        list(fk_row.values())[:num_columns] for fk_row in fk_list
                    ]

                    # store
                    fk_data[
                        fk["REFERENCED_TABLE_NAME"] + "." + fk["REFERENCED_COLUMN_NAME"]
                    ] = fk_list

                # store
                columns_data[column_name] = {
                    "type": column_type,
                    "name": column_name,
                    "foreign_keys": fk_data,
                    "key_type": fk_data,
                }

            return columns_data

        return self.run_query(
            f"SHOW COLUMNS FROM {table};",
            callback=lambda records: process_columns_data(table, records),
        )

    # read records from given table
    def read(self, table):
        return self.run_query(f"SELECT * FROM {table};")

    # create a new record in the given table
    def create(self, table, data):
        # Ensure that 'data' is a dictionary where keys are column names
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        return self.run_query(query, data)

    def close_connection(self):
        """Close the database connection if open."""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def run_query(self, query, query_params=None, callback=None):
        """
        Run a query on the database and return the result.
        If a callback is present, pass the result to the callback first and return that result.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)

            if query_params != None:
                cursor.execute(query, tuple(query_params.values()))
            else:
                cursor.execute(query)

            records = cursor.fetchall()  # format: list of dictionaries
            if callback == None:
                return records
            else:
                return callback(records)

        except Error as e:
            print(f"Error reading records: {e}")
            return []
        finally:
            self.connection.commit()
            cursor.close()
