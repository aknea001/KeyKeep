from backend import backend, passgen, encrypt
import art
from pwinput import pwinput
from time import sleep
import os
from os.path import join, dirname, abspath
import sys

def main():
    dirPath = dirname(abspath(__file__))

    while True:
        user = str(input("Username: "))
        x = pwinput("Master Password: ")

        rightMaster = backend.rightMaster(x, user)

        if rightMaster[0]:
            os.system("clear")
            salt = backend.getSalt(user)[1]
            kek = encrypt.pbkdf2(x.encode(), salt.encode(), 100000, 32)
            AESkey = encrypt.decryptDek(kek, rightMaster[2], rightMaster[1])
            break
        else:
            print("Wrong Password.. \nTry again..")

    while True:
        art.table(backend.tableInfo(user))
        x = str(input(">> ")).strip().lower()
        if x == "exit":
            break
        elif x == "clear":
            os.system("clear")
        elif x == "restart":
            os.system("clear")
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif x == "new":
            title = str(input("Title / Site: "))
            username = str(input("Username: "))
            password = str(input("Password* (default: random): "))

            if password == "":
                with open(join(dirPath, "randOptions.txt"), "r") as f:
                    options = f.readlines()

                defLength = options[0].strip().split("=")[1]
                defRemove = options[1].strip().split("=")[1]

                while True:
                    try:
                        passlen = int(input(f"\nPassword Length (default: {defLength}): "))
                        break
                    except ValueError:
                        passlen = defLength
                        break

                removeChar = str(input(f"Characters to exclude (seperated by space) (default: {defRemove}): "))
                if removeChar == "":
                    removeChar = defRemove

                remove = removeChar.split(" ")
                remove = None if removeChar == "None" else remove

                keepOpt = str(input("Save Options to default [y / n] (default: y): ").lower())
                if keepOpt != ("n" or "no"):
                    with open(join(dirPath, "randOptions.txt"), "w") as f:
                        f.write(f"len={passlen}\nremove={removeChar}")

                password = passgen.generatePass(passlen, remove)
                
            backend.insert(user, AESkey, password, title or None, username or None)
        elif x.startswith("get"):
            headless = False

            if " -h" in x:
                headless = True

                xLst = x.split(" ")
                try:
                    xLst.remove("-h")
                except ValueError:
                    print("need to seperate id and '-h'")
                    continue

                x = " ".join(xLst)

            try:
                xLst = x.split(" ")
                upID = int(xLst[1])
                backend.get(AESkey, upID, user, headless)
                sleep(1)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                upID = int(input("ID: "))
                backend.get(AESkey, upID, user, headless)
                sleep(1)
            except ValueError:
                print("Has to be a whole number..")
        elif x.startswith("rm"):
            try:
                xLst = x.split(" ")
                pID = int(xLst[1])
                backend.remove(pID, user)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                pID = int(input("ID: "))
                backend.remove(pID)
            except ValueError:
                print("Has to be a whole number..")
        elif x.startswith("update"):
            try:
                xLst = x.split(" ")
                pID = int(xLst[1])
            except ValueError:
                print("Has to be a whole number..")
                continue
            except IndexError:
                try:
                    pID = int(input("ID: "))
                except ValueError:
                    print("Has to be a whole number..")
                    continue

            newPass = str(input("New password: "))
            backend.update(user, AESkey, pID, newPass)
        elif x == "adduser":
            name = str(input("Username: "))
            passwd = pwinput("Master Password: ")

            backend.addUser(name, passwd)

if __name__ == "__main__":
    main()