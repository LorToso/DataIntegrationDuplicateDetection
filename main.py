import csv
with open("D:\home\MEGA\TU-Berlin\Data Integration\DuplicateDetection\inputDB.csv") as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        print(', '.join(row))


