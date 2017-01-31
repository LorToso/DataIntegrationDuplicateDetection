import csv
import re

def getSSNcluster(file):
    with open(file) as csv_file:
        file_reader = csv.reader(csv_file)
        next(file_reader, None)
        rows = []
        non_decimal = re.compile(r'[^\d.]+')
        for row in file_reader:
            if not len(row[-2]) == 0:
                row[-2] = non_decimal.sub('', row[-2])
                rows.append([row[0], int(row[-2])])
        values = set(map(lambda x: x[1], rows))
        clusters = [[y[0] for y in rows if y[1] == x] for x in values]
        return clusters

clusters = getSSNcluster("inputDB.csv")

output = ""
for i in range(len(clusters)):
    for j in range(len(clusters[i])):
        output += str(i) + "," + clusters[i][j] + "\n"

f = open("ssnCluster", 'w')
f.write(output)
f.close()



