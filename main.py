import sqlconnect

def main():
    while True:
        x = str(input(">> "))
        if x == "exit":
            break
        elif x == "new":
            title = str(input("Title: "))
            username = str(input("Username: "))
            password = str(input("Password: "))

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