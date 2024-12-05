#import sqlconnect

def table(lst):
    maxlens = {}

    maxLen = None

    for el in lst:
        print(el)
        for i in range(len(el)):
            if maxLen == None:
                maxLen = 0
            print(i)
            if len(el[i]) > maxLen:
                maxLen = len(el[i])

            print(maxLen)

            maxlens[i] = maxLen + 2

    print(maxlens)

    column = ["ID", "Title", "Username"]
    for i in range(len(lst[0])):
        if maxlens[i] < len(column[i]) + 2:
            maxlens[i] = len(column[i]) + 2

    print(maxlens)

    for i in range(len(lst[0])):
        print(f"+{'-' * maxlens[i]}", end="")
    print("+")

    for i in range(len(lst[0])):
        print(f"| {column[i]}{' ' * (maxlens[i] - len(column[i]) - 1)}", end="")
    
    print("|")

    for i in range(len(lst[0])):
        print(f"+{'-' * maxlens[i]}", end="")
    print("+")

    for item in lst:
        for i in range(len(item)):
            print(f"| {item[i]}{' ' * (maxlens[i] - len(item[i]) - 1)}", end="")
        
        print("|")

    for i in range(len(lst[0])):
        print(f"+{'-' * maxlens[i]}", end="")
    print("+")

lst = [("1", 'Testing yk yk', "None"), ("2", 'Testing', "None"), ("3", 'None', "None")]
table(lst)
#print(sqlconnect.getInfo())