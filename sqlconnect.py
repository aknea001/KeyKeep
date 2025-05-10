from dotenv import load_dotenv
from os import getenv
import mysql.connector

load_dotenv()

sqlconfig = {
    "host": getenv("SQLHOST"),
    "user": getenv("SQLUSER"),
    "password": getenv("SQLPASSWD"),
    "database": getenv("SQLDATABASE")
}

def pad(s):
    padding = 16 - len(s) % 16
    return s + padding * chr(padding)

def unpad(s):
    padVerdi = s[-1]
    return s[:-padVerdi]

def insert(user, key, passwd, title=None, usrname=None):
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    import base64
        
    iv = get_random_bytes(16)

    passwd = pad(passwd).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encryptedPass = cipher.encrypt(passwd)

    b64EncryptedPass = base64.b64encode(encryptedPass)
    b64iv = base64.b64encode(iv)

    uID = getuID(user)

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "INSERT INTO passwds (password, iv, title, username, userID)\
                VALUES\
                (%s, %s, %s, %s, %s)"
        
        cursor.execute(query, (b64EncryptedPass, b64iv, title, usrname, uID))
        db.commit()

        print("Successfully inserted into db..")
    except mysql.connector.Error as e:
        print(f"sqlconnect insert ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def update(user, key, upID, passwd, title=None, usrname=None):
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    import base64

    iv = get_random_bytes(16)

    passwd = pad(passwd).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encryptedPass = cipher.encrypt(passwd)

    b64EncryptedPass = base64.b64encode(encryptedPass)
    b64iv = base64.b64encode(iv)

    uID = getuID(user)
    pID = tranUpID(upID, uID)

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "UPDATE passwds\
                SET password = %s, iv = %s\
                WHERE id = %s AND userID = %s"
        
        cursor.execute(query, (b64EncryptedPass, b64iv, pID, uID))
        db.commit()

        print("Successfully updated password..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnector update ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()
    

def get(key, upID, user, headless: bool):
    from Crypto.Cipher import AES
    import base64
    import threading
    import pyperclip
    from time import sleep
    import os

    uID = getuID(user)
    pID = tranUpID(upID, uID)

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
        
        def revertHeadless():
            sleep(30)

            os.remove("password.key")
        
        def revertClip():
            sleep(10)

            pyperclip.copy("")
        
        if headless:
            with open("password.key", "w") as f:
                f.write(decrypted)

            print("Wrote password to 'password.key' \nWill delete in 30 sec..")

            headlessThread = threading.Thread(target=revertHeadless, daemon=True)
            headlessThread.start()
            return

        try:
            pyperclip.copy(decrypted)
        except pyperclip.PyperclipException:
            print("failed adding password to clipboard.. \nIf you're in a headless environment, use '-h' option to save to file instead")
            return

        if decrypted == "":
            print("Wrong key..")
        else:
            print("Added password to your clipboard.. \nWill clear in 10 sec..")

        thread1 = threading.Thread(target=revertClip, daemon=True)
        thread1.start()
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect get ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def remove(upID, user):
    uID = getuID(user)
    pID = tranUpID(upID, uID)
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "DELETE FROM passwds WHERE id = %s AND userID = %s"
        cursor.execute(query, (pID, uID))

        db.commit()
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect remove ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def addUser(name, passwd):
    import hashlib
    import base64
    from secrets import token_hex

    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    import encrypt

    salts = f"{token_hex(32)} {token_hex(32)}"
    flavorPass = passwd + str(salts.split(" ")[0])
    hashed = hashlib.sha256(flavorPass.encode()).hexdigest()

    b64salts = base64.b64encode(salts.encode())

    kek = encrypt.pbkdf2(passwd.encode(), salts.split(" ")[1].encode(), 100000, 32)
    dek = get_random_bytes(32)
    iv = get_random_bytes(16)

    cipher = AES.new(kek, AES.MODE_CBC, iv)
    dekCiphertext = cipher.encrypt(dek)

    b64Dek = base64.b64encode(dekCiphertext)
    b64iv = base64.b64encode(iv)

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "INSERT INTO users (username, hash, salt, dek, iv)\
                VALUES\
                (%s, %s, %s, %s, %s)"
        
        cursor.execute(query, (name, hashed, b64salts, b64Dek, b64iv))
        db.commit()

        print(f"Successfully added {name}..")
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect addUser ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def rightMaster(passInput, username) -> list:
    import hashlib

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT hash, dek, iv FROM users WHERE username = %s"
        cursor.execute(query, (username, ))
        data = cursor.fetchall()[0]
        correctHash = data[0]
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect rightMaster ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

    salt = getSalt(username)[0]
    passInput += str(salt)
    
    hashObject = hashlib.sha256(str(passInput).encode())
    hashed = hashObject.hexdigest()

    if hashed == correctHash:
        return [True, data[1], data[2]]
    else:
        return [False]

def tableInfo(username):
    uID = getuID(username)
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT title, username from passwds WHERE userID = %s"
        cursor.execute(query, (uID, ))

        info = cursor.fetchall()

        goodInfo = []

        for el in info:
            goodInfo.append(list(map(str, el)))

        return goodInfo
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect getInfo ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def getSalt(username):
    import base64

    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT salt FROM users WHERE username = %s"
        cursor.execute(query, (username, ))

        b64salts = cursor.fetchone()[0]

        salts = base64.b64decode(b64salts).decode()
        saltsLst = salts.split(" ")

        return saltsLst
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect getSalt ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def getuID(username):
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username, ))

        uID = cursor.fetchone()[0]

        return uID
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect getuID ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

def tranUpID(upID, uID):
    try:
        db = mysql.connector.connect(**sqlconfig)
        cursor = db.cursor()

        query = "SELECT id FROM passwds WHERE userID = %s"
        cursor.execute(query, (uID, ))

        ids = cursor.fetchall()

        return ids[upID - 1][0]
    except mysql.connector.Error as e:
        db = None
        print(f"sqlconnect delete ERROR: {e}")
    finally:
        if db != None and db.is_connected():
            db.close()
            cursor.close()

if __name__ == "__main__":
    addUser("del", "password")