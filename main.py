import sqlconnect

def main():
    x = str(input(">> "))
    if x == "new":
        title = str(input("Title: \n>> "))
        username = str(input("Username: \n>> "))
        password = str(input("Password: \n>> "))

        sqlconnect.insert(password, title or None, username or None)


if __name__ == "__main__":
    main()