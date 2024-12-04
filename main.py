import sqlconnect

def main():
    while True:
        x = str(input("\n\n>> "))
        if x == "exit":
            break
        elif x == "new":
            title = str(input("Title: "))
            username = str(input("Username: "))
            password = str(input("Password: "))

            sqlconnect.insert(password, title or None, username or None)
        elif x == "get":
            try:
                pID = int(input("ID: "))
                sqlconnect.get(pID)
            except ValueError:
                print("Has to be a whole number..")

if __name__ == "__main__":
    main()