from dotenv import load_dotenv
from os import getenv
import mysql.connector

load_dotenv()

sqlconfig = {
    "host": getenv("SQLHOST"),
    "user": getenv("SQLUSER"),
    "password": getenv("SQLPASSWD"),
    "database": getenv("DATABASE")
}

def insert(passwd, title=None, usrname=None):
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "INSERT INTO passwds (password, title, username)\
                VALUES\
                (%s, %s, %s)"
        
        cursor.execute(query, (passwd, title, usrname))
        db.commit()

        print("Successfully inserted into db..")
    except mysql.connector.Error as e:
        return f"sqlconnect insert ERROR: {e}"
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()