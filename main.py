import sqlconnect

def main():
    x = str(input(">> "))
    if x == "new":
        title = str(input("Title: "))
        username = str(input("Username: "))
        password = str(input("Password: "))

        sqlconnect.insert(password, title or None, username or None)

if __name__ == "__main__":
    main()