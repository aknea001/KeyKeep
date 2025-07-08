from backend.databaseConnection import Database

db = Database()

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
        query = "INSERT INTO passwds (password, iv, title, username, userID)\
                VALUES\
                (%s, %s, %s, %s, %s)"
        
        db.execute(query, b64EncryptedPass, b64iv, title, usrname, uID)

        print("Successfully inserted into db..")
    except ConnectionError as e:
        print(f"sqlconnect insert ERROR: {e}")
        return

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
        query = "UPDATE passwds\
                SET password = %s, iv = %s\
                WHERE id = %s AND userID = %s"
        
        db.execute(query, b64EncryptedPass, b64iv, pID, uID)

        print("Successfully updated password..")
    except ConnectionError as e:
        print(f"sqlconnector update ERROR: {e}")
        return

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
        query = "SELECT password, iv FROM passwds WHERE id = %s"
        x = db.execute(query, pID)[0]
    except ConnectionError as e:
        print(f"sqlconnect get ERROR: {e}")
        return

    b64password = base64.b64decode(x["password"])
    b64iv = base64.b64decode(x["iv"])

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
        return
    else:
        print("Added password to your clipboard.. \nWill clear in 10 sec..")

    thread1 = threading.Thread(target=revertClip, daemon=True)
    thread1.start()

def remove(upID, user):
    uID = getuID(user)
    pID = tranUpID(upID, uID)
    try:
        query = "DELETE FROM passwds WHERE id = %s AND userID = %s"
        db.execute(query, pID, uID)
    except ConnectionError.connector.Error as e:
        print(f"sqlconnect remove ERROR: {e}")
        return

def addUser(name, passwd):
    import hashlib
    import base64
    from secrets import token_hex

    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from backend import encrypt

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
        query = "INSERT INTO users (username, hash, salt, dek, iv)\
                VALUES\
                (%s, %s, %s, %s, %s)"
        
        db.execute(query, name, hashed, b64salts, b64Dek, b64iv)

        print(f"Successfully added {name}..")
    except ConnectionError as e:
        print(f"sqlconnect addUser ERROR: {e}")
        return

def rightMaster(passInput, username) -> list:
    import hashlib

    try:
        query = "SELECT hash, dek, iv FROM users WHERE username = %s"
        data = db.execute(query, username)[0]
    except ConnectionError as e:
        print(f"sqlconnect rightMaster ERROR: {e}")
        return

    correctHash = data["hash"]

    salt = getSalt(username)[0]
    passInput += str(salt)
    
    hashObject = hashlib.sha256(str(passInput).encode())
    hashed = hashObject.hexdigest()

    if hashed == correctHash:
        return [True, data["dek"], data["iv"]]
    else:
        return [False]

def tableInfo(username):
    uID = getuID(username)
    try:
        query = "SELECT title, username from passwds WHERE userID = %s"
        info = db.execute(query, uID)
    except ConnectionError as e:
        print(f"sqlconnect getInfo ERROR: {e}")
        return

    goodInfo = []

    for el in info:
        goodInfo.append([el["title"], el["username"]])

    return goodInfo

def getSalt(username):
    import base64

    try:
        query = "SELECT salt FROM users WHERE username = %s"
        b64salts = db.execute(query, username)[0]["salt"]
    except ConnectionError as e:
        print(f"sqlconnect getSalt ERROR: {e}")
        return
    
    salts = base64.b64decode(b64salts).decode()
    saltsLst = salts.split(" ")

    return saltsLst

def getuID(username):
    try:
        query = "SELECT id FROM users WHERE username = %s"
        uID = db.execute(query, username)
    except ConnectionError as e:
        print(f"sqlconnect getuID ERROR: {e}")
        return
    
    return uID[0]["id"]

def tranUpID(upID, uID):
    try:
        query = "SELECT id FROM passwds WHERE userID = %s"
        ids = db.execute(query, uID)
    except ConnectionError as e:
        print(f"sqlconnect delete ERROR: {e}")
        return
    
    return ids[upID - 1]["id"]