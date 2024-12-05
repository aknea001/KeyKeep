lst = [(None, "null", 1), ("hei", "på", "deg"), (None, None, None), (1, 2, 3)]
newLst = []

for el in lst:
    newLst.append(list(map(str, el)))

print(newLst)