import csv
with open("D:\home\MEGA\TU-Berlin\Data Integration\DuplicateDetection\inputDB.csv") as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        print(', '.join(row))


