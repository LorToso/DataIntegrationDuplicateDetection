import Levenshtein as lv
import statistics
import csv
import operator

with open("smalltest.csv") as csvfile:
    filereader = csv.reader(csvfile)
    rows = []
    for row in filereader:
        rows.append(row)

    rows = rows[1:]

distanceMeasureMethodCount = 6
approaches = ['distance', 'jaro', 'jaro_winkler', 'ratio', 'seqratio', 'setratio']
rowcount = len(rows)
colcount = len(rows[0])
comparisons = int((rowcount * rowcount - rowcount) / 2)

res = [[0 for x in range(2 + distanceMeasureMethodCount)] for x in range(comparisons)]
i = 0

for cand1 in range(0, 100):
    for cand2 in range(cand1 + 1, len(rows)):
        cand1Str = ''
        cand2Str = ''
        for col in range(0, colcount):
            if (rows[cand1][col] != '') & (rows[cand2][col] != ''):
                val1 = rows[cand1][col].upper()
                val2 = rows[cand2][col].upper()
                if col == 1 | col == 3:
                    val1 = val1 + val1 + val1  # this basically adds weight 3 to the names
                    val2 = val2 + val2 + val2  # this basically adds weight 3 to the names
                cand1Str += val1
                cand2Str += val2

        res[i][0] = lv.distance(cand1Str, cand2Str)
        res[i][1] = lv.jaro(cand1Str, cand2Str)
        res[i][2] = lv.jaro_winkler(cand1Str, cand2Str)
        res[i][3] = lv.ratio(cand1Str, cand2Str)
        res[i][4] = lv.seqratio(cand1Str, cand2Str)
        res[i][5] = lv.setratio(cand1Str, cand2Str)
        res[i][-2] = cand1
        res[i][-1] = cand2
        i += 1
        if i % 1000 == 0:
            print(i)

res = res[:(i - 1)]

for approach in range(distanceMeasureMethodCount):
    distances = [row[approach] for row in res]
    min_index, min_value = min(enumerate(distances), key=operator.itemgetter(1))
    max_index, max_value = max(enumerate(distances), key=operator.itemgetter(1))

    val = min_value if approach in [0] else max_value
    index = min_index if approach in [0] else max_index
    print('Minimum ' + approaches[approach] + ': ' + str(val) + ' for tuples:\n' + str(
        rows[res[index][-2]]) + ' \n->\n' + str(rows[res[index][-1]]))
