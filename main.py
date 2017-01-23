import Levenshtein as lv
import statistics
import csv
import time

with open("smallInput.csv") as csvfile:
    filereader = csv.reader(csvfile)
    list = []
    for row in filereader:
        list.append(row)

    res = []
    start_time = time.time()

    for cand1 in range(1, len(list) - 1):
        for cand2 in range(cand1 + 1, len(list)):
            res.append(lv.distance(str(list[cand1]).upper(), str(list[cand2]).upper()))

    elapsed_time = time.time() - start_time

    print('Minimum: ' + str(min(res)))
    print('Maximum: ' + str(max(res)))
    print('Median: ' + str(statistics.median(res)))
    print('Elapsed Time: {time} seconds '.format(time=str(elapsed_time)))
