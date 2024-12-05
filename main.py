import sqlconnect
import art
from pwinput import pwinput
from os import system

def main():
    while True:
        x = pwinput("Master Password: ")

        if sqlconnect.rightMaster(x):
            system("clear") or system("cls")
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
            password = str(input("Password*: "))

            sqlconnect.insert(password, title or None, username or None)
        elif x.startswith("get"):
            try:
                xLst = x.split(" ")
                pID = int(xLst[1])
                sqlconnect.get(pID)
                continue
            except IndexError:
                pass
            except ValueError:
                print("Has to be a whole number..")
                continue

            try:
                pID = int(input("ID: "))
                sqlconnect.get(pID)
            except ValueError:
                print("Has to be a whole number..")

if __name__ == "__main__":
    main()