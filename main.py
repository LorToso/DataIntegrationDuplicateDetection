import Levenshtein as lv
import statistics
import csv

with open("smallInput.csv") as csvfile:
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
            if i % 10000 == 0:
                print(i)
    print('Minimum: ' + str(min(res)))
    print('Maximum: ' + str(max(res)))
    print('Median: ' + str(statistics.median(res)))
