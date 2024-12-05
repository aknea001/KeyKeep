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
    for i in range(1, len+1):
        passwd += choice(charLst)

    return passwd