import Levenshtein as lv
import csv
with open("inputDB.csv") as csvfile:
    filereader = csv.reader(csvfile)
    list = []
    for row in filereader:
        list.append(row)
    #for row in list:
        #print(row)
print(lv.distance('abc', 'abd'))


