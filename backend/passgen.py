def getChars(remove=None):
    import string

    charLst = []

    for i in string.ascii_letters:
        charLst.append(i)

    for i in string.digits:
        charLst.append(i)

    for i in string.punctuation:
        charLst.append(i)

    if remove != None:
        for i in remove:
            charLst.remove(i)

    return charLst

def generatePass(len, rm=None):
    from random import choice

    charLst = getChars(rm)

    passwd = ""
    for i in range(1, int(len)+1):
        passwd += choice(charLst)

    return passwd

def goodPass(passwd):
    import string

    if len(passwd) >= 15:
        return True

    richard = {}

    for i in passwd:
        if i in string.ascii_lowercase and "lower" not in richard:
            richard["lower"] = 1
        elif i in string.ascii_uppercase and "upper" not in richard:
            richard["upper"] = 1
        elif i in string.digits and "digits" not in richard:
            richard["digits"] = 1
        elif i in string.punctuation and "punc" not in richard:
            richard["punc"] = 1

    if len(richard) == 4:
        return True
    else:
        print("False")
        return False