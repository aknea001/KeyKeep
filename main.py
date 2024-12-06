import sqlconnect
import art
import passgen
import encrypt
from pwinput import pwinput
from os import system
from time import sleep

def main():
    while True:
        x = pwinput("Master Password: ")

        if sqlconnect.rightMaster(x):
            system("clear")
            break
        else:
            print("Wrong Password.. \nTry again..")

    while True:
        art.table(sqlconnect.getInfo())
        x = str(input(">> ")).strip()
        if x == "exit":
            break
        elif x == "clear":
            system("clear")
        elif x == "new":
            title = str(input("Title / Site: "))
            username = str(input("Username: "))
            password = str(input("Password* (default: random): "))

            if password == "":
                with open("randOptions.txt", "r") as f:
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
                    with open("randOptions.txt", "w") as f:
                        f.write(f"len={passlen}\nremove={removeChar}")

            password = passgen.generatePass(passlen, remove)
            sqlconnect.insert(password, title or None, username or None)
        elif x.startswith("get"):
            try:
                xLst = x.split(" ")
                pID = int(xLst[1])
                sqlconnect.get(pID)
                sleep(1)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                pID = int(input("ID: "))
                sqlconnect.get(pID)
                sleep(1)
            except ValueError:
                print("Has to be a whole number..")

if __name__ == "__main__":
    main()