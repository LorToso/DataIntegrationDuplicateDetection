import Levenshtein as lv
import statistics
import csv
import operator
import time

with open("smallInput.csv") as csvfile:
    filereader = csv.reader(csvfile)
    rows = []
    for row in filereader:
        rows.append(row)

    rows = rows[1:]

rowcount = len(rows)
comparisons = int((rowcount * rowcount - rowcount) / 2)

res = [[0 for x in range(3)] for x in range(comparisons)]
i = 0
start_time = time.time()


for cand1 in range(0, len(rows) - 1):
    for cand2 in range(cand1 + 1, len(rows)):
        dist = lv.distance(str(rows[cand1]).upper(), str(rows[cand2]).upper())
        res[i][0] = dist
        res[i][1] = cand1
        res[i][2] = cand2
        i += 1

elapsed_time = time.time() - start_time

distances = [row[0] for row in res]
min_index, min_value = min(enumerate(distances), key=operator.itemgetter(1))
max_index, max_value = max(enumerate(distances), key=operator.itemgetter(1))

print('Minimum: ' + str(min_value) + ' for tuples:\n' + str(rows[res[min_index][1]]) + ' \n->\n' + str(rows[res[min_index][2]]))
print('Maximum: ' + str(max_value) + ' for tuples:\n' + str(rows[res[max_value][1]]) + ' \n->\n' + str(rows[res[max_value][2]]))
print('Median: ' + str(statistics.median(res)))
print('Elapsed Time: {time} seconds '.format(time=str(elapsed_time)))
