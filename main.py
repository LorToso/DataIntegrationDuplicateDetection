import Levenshtein as lv
import csv

with open("inputDB.csv") as csvfile:
    filereader = csv.reader(csvfile)
    list = []
    for row in filereader:
        list.append(row)

    res = []
    i = 0
    for cand1 in range(1, len(list) - 1):
        for cand2 in range(cand1 + 1, len(list)):
            res.append(lv.distance(''.join(list[cand1]), ''.join(list[cand2])))
            i += 1
            if i % 100 == 0:
                print(i)
