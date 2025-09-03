def table(lst):
    from os.path import join, dirname, abspath

    try:
        count = 1
        for el in lst:
            el.insert(0, str(count))
            count += 1

        maxlens = {}

        for i in range(len(lst[0])):
            maxlens[i] = 0

        for el in lst:
            for i in range(len(el)):
                if len(str(el[i])) + 2 > maxlens[i]:
                    maxlens[i] = len(str(el[i])) + 2

        column = ["ID", "Title", "Username"]
        for i in range(len(lst[0])):
            if maxlens[i] < len(column[i]) + 2:
                maxlens[i] = len(column[i]) + 2

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
                print(f"| {item[i]}{' ' * (maxlens[i] - len(str(item[i])) - 1)}", end="")
            
            print("|")

        for i in range(len(lst[0])):
            print(f"+{'-' * maxlens[i]}", end="")
        print("+")
    except IndexError:
        with open(join(dirname(abspath(__file__)), "emptyTable.txt")) as f:
            print(f.read())

        print("'New' to add entry")