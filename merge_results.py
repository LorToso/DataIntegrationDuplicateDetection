import os
import csv


def read_csv(file):
    with open(file) as csv_file:
        file_reader = csv.reader(csv_file)
        rows = []
        for row in file_reader:
            rows.append(row)
        return rows

allFiles = []
clusters = []
newClusterID = 1

for fn in os.listdir('.'):
    if os.path.isfile(fn):
        if fn.startswith("out."):
            rows = read_csv(fn)
            allFiles.append(rows)

i = 0
for dataset in allFiles:
    while len(dataset) > 0:
        row1 = dataset[0]
        ids_in_same_cluster = set(map(lambda r: r[1], filter(lambda r: r[0] == row1[0], dataset)))
        clusters.append(ids_in_same_cluster)

        newClusterID += 1

        dataset[:] = [r for r in dataset if r[1] not in ids_in_same_cluster]
        if newClusterID % 1000 == 0:
            print("clusters: " + str(newClusterID))
    print("dataset: " + str(i))
    i += 1


something_changed = True
while something_changed:
    something_changed = False
    i = 0
    j = 0
    while i < (len(clusters)-1):
        if(i % 100 == 0): print("Merging Cluster:" + str(i))
        cl1 = clusters[i]

        j = i+1
        while j < len(clusters):
            cl2 = clusters[j]
            if len(cl1 & cl2) > 0:
                cl1 = cl1 | cl2
                clusters[j] = set()
                something_changed = True
            j += 1

        i += 1

    print("done with run")
cluster_id = 1


with open('final_out.csv', 'w+') as file:
    for cluster in clusters:
        if len(cluster) == 0:
            continue
        for id in cluster:
            file.write(str(cluster_id) + ',' + str(id) + '\n')
        cluster_id += 1

