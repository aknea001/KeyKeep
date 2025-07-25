from mysql.connector import pooling, Error as mysqlError
from dotenv import load_dotenv
from os import getenv

class Database():
    def __init__(self):
        load_dotenv()

        self.dbConfig = {
            "host": getenv("SQLHOST"),
            "user": getenv("SQLUSER"),
            "password": getenv("SQLPASSWD"),
            "database": getenv("SQLDATABASE")
        }

        self.pool = pooling.MySQLConnectionPool (
            pool_name = "mypool",
            pool_size = 5,
            **self.dbConfig
        )
    
    def execute(self, query: str, *args):
        values = tuple(args)
        connection = None
        cursor = None

        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, values)

            if query.upper().startswith("SELECT"):
                data = cursor.fetchall()
                
                return data
            
            connection.commit()

            return cursor.lastrowid
        except mysqlError as e:
            raise ConnectionError(e)
        finally:
            if connection:
                connection.close()

            if cursor:
                cursor.close()