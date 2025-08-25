from backend import passgen
import art
from api.api import Api
from pwinput import pwinput
from time import sleep
from dotenv import load_dotenv
import os
from os.path import join, dirname, abspath
import sys

load_dotenv()

def main():
    dirPath = dirname(abspath(__file__))

    exBackend = os.getenv("externalBackend")
    host = os.getenv("SQLHOST")
    port = os.getenv("SQLPORT")

    if exBackend == "a":
        api = Api(True, host, port)
    elif exBackend == "f":
        api = Api(False)
    else:
        askExBackend = str(input("Do you want to use an external backend? [y/n] (Default: n): "))

        if askExBackend == "y":
            api = Api(True, host, port)
        else:
            api = Api(False)

    while True:
        user = str(input("Username: "))
        x = pwinput("Master Password: ")

        rightMaster = api.login(user, x)

        if rightMaster:
            os.system("clear")
            break
        else:
            print("Wrong Password.. \nTry again..")

    while True:
        art.table(api.tableData()["data"])
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
                
            api.insert(password, title or None, username or None)
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
                api.get(upID, headless)
                sleep(1)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                upID = int(input("ID: "))
                api.get(upID, headless)
                sleep(1)
            except ValueError:
                print("Has to be a whole number..")
        elif x.startswith("rm"):
            try:
                xLst = x.split(" ")
                pID = int(xLst[1])
                api.remove(pID)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                pID = int(input("ID: "))
                api.remove(pID)
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
            api.update(pID, newPass)
        elif x == "adduser":
            name = str(input("Username: "))
            passwd = pwinput("Master Password: ")

            api.addUser(name, passwd)

if __name__ == "__main__":
    main()