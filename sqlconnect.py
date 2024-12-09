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

def close(db, cursor):
    if db != None and db.is_connected():
            cursor.close()
            db.close()

def insert(key, passwd, title=None, usrname=None):
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    import base64
        
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

        print("Successfully inserted into db..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect insert ERROR: {e}")
    finally:
        close(db, cursor)

def get(key, pID):
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

        cipher = AES.new(key, AES.MODE_CBC, b64iv)
        decrypted = cipher.decrypt(b64password)
        try:
            decrypted = unpad(decrypted).decode()
        except UnicodeDecodeError:
            print("ERROR: wrong key or problem with system..")
            return

        root = Tk()
        root.withdraw()
        root.clipboard_append(decrypted)

        if decrypted == "":
            print("Wrong key..")
        else:
            print("Added password to your clipboard..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect get ERROR: {e}")
    finally:
        close(db, cursor)

def remove(pID):
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "DELETE FROM passwds WHERE id = %s"
        cursor.execute(query, (pID, ))

        db.commit()
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect remove ERROR: {e}")
    finally:
        close(db, cursor)

def rightMaster(passInput):
    import hashlib

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT hash FROM users WHERE id = %s"
        cursor.execute(query, (1, ))
        correctHash = cursor.fetchone()[0]
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect rightMaster ERROR: {e}")
    finally:
        close(db, cursor)

    salt = getSalt()[0]
    passInput += str(salt)
    
    hashObject = hashlib.sha256(str(passInput).encode())
    hashed = hashObject.hexdigest()

    if hashed == correctHash:
        return True
    else:
        return False

def getInfo():
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT id, title, username from passwds"
        cursor.execute(query)

        info = cursor.fetchall()

        goodInfo = []

        for el in info:
            goodInfo.append(list(map(str, el)))

        return goodInfo
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect getInfo ERROR: {e}")
    finally:
        close(db, cursor)

def getSalt():
    import base64

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT salt FROM users WHERE id = %s"
        cursor.execute(query, (1, ))

        b64salts = cursor.fetchone()[0]

        salts = base64.b64decode(b64salts).decode()
        saltsLst = salts.split(" ")

        return saltsLst
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect getSalt ERROR: {e}")
    finally:
        close(db, cursor)

if __name__ == "__main__":
    print(rightMaster("password"))