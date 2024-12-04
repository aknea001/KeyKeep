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

def pad(s):
    padding = 16 - len(s) % 16
    return s + padding * chr(padding)

def unpad(s):
    padVerdi = s[-1]
    return s[:-padVerdi]

def insert(passwd, title=None, usrname=None):
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    import base64

    try:
        with open(".key/key.bin", "rb") as f:
            key = f.read()
    except FileNotFoundError:
        key = get_random_bytes(16)
        
    iv = get_random_bytes(16)

    passwd = pad(passwd).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encryptedPass = cipher.encrypt(passwd)

    b64EncryptedPass = base64.b64encode(encryptedPass)
    b64iv = base64.b64encode(iv)

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "INSERT INTO passwds (password, iv, title, username)\
                VALUES\
                (%s, %s, %s, %s)"
        
        cursor.execute(query, (b64EncryptedPass, b64iv, title, usrname))
        db.commit()

        with open(".key/key.bin", "wb") as f:
            f.write(key)

        print("Successfully inserted into db..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect insert ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

def get(pID):
    from Crypto.Cipher import AES

    import base64

    from tkinter import Tk

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT password, iv FROM passwds WHERE id = %s"
        cursor.execute(query, (pID, ))
        x = cursor.fetchone()

        b64password = base64.b64decode(x[0])
        b64iv = base64.b64decode(x[1])
        
        with open(".key/key.bin", "rb") as f:
            key = f.read()

        cipher = AES.new(key, AES.MODE_CBC, b64iv)
        decrypted = cipher.decrypt(b64password)
        decrypted = unpad(decrypted).decode()

        root = Tk()
        root.withdraw()
        root.clipboard_append(decrypted)

        print("Added password to your clipboard..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect get ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    get(1)