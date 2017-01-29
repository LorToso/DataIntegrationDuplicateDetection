import Levenshtein as lv
import csv
import time
import multiprocessing as mp

rows_to_deduplicate = 0
rows_to_compare_to = 0
col_count = 0
name_weight = 5
rows = []
comparisons_performed = 0
res = []

dict_res = {} # key=(tuple0, tuple1), value = distance


def deduplicate(infile, outfile):
    global rows_to_deduplicate, rows_to_compare_to, col_count, rows, res, comparisons_performed
    rows = read_csv(infile)

    approaches = ['distance', 'jaro', 'jaro_winkler', 'ratio', 'seqratio', 'setratio']
    distance_measure_method_count = len(approaches)

    row_count = len(rows)
    col_count = len(rows[0])

    # The following variables are just for testing purposes
    # rows_to_deduplicate = 10
    # rows_to_compare_to = 20000
    rows_to_deduplicate = row_count
    rows_to_compare_to = row_count
    # name_weight = 5

    # comparisons_needed = int(rows_to_compare_to * rows_to_deduplicate
    #                          - (rows_to_deduplicate * rows_to_deduplicate - rows_to_deduplicate) / 2)

    # res = allocate_result_table(comparisons_needed, distance_measure_method_count)

    start_time = time.time()

    perform_comparisons()
    # this makes sure the result set does not have more entries than needed.
    # Theoretically this is unnecessary, but its neat for testing purposes
    # res = res[:(comparisons_performed - 1)]

    elapsed_time = time.time() - start_time

    checked_metric = 3
    threshold = 0.85

    # duplicates = list(filter(lambda r: r[checked_metric] > threshold, res))

    # print_possible_duplicates(checked_metric, duplicates, rows)

    # clusters = create_duplicate_clusters(duplicates, rows)

    # sorted_clusters = to_sorted_cluster_list(clusters)

    # print_clusters(sorted_clusters)

    # write_clusters_to_file(outfile, sorted_clusters)

    print_dict()

    print('Elapsed Time: {time} seconds '.format(time=str(elapsed_time)))
    # print('Comparisons Performed: {comparisons}'.format(comparisons=comparisons_performed))


def write_clusters_to_file(outfile, sorted_clusters):
    f = open(outfile, 'w')
    for row in sorted_clusters:
        f.write(str(row[0]) + "," + str(row[1]) + '\n')
    f.close()


def print_clusters(sorted_clusters):
    for row in sorted_clusters:
        print(str(row[0]) + ", " + str(row[1]))


def to_sorted_cluster_list(clusters):
    cluster_list = alloc_2d_list(len(clusters), 2)
    i = 0
    for record_id, cluster in clusters.items():
        cluster_list[i][0] = cluster
        cluster_list[i][1] = record_id
        i += 1
    sorted_clusters = sorted(cluster_list, key=lambda r: r[0])
    return sorted_clusters


def create_duplicate_clusters(duplicates, rows):
    clusters = {}
    cluster_id = 1
    for result in duplicates:
        tuple_0_id = rows[result[-2]][0]
        tuple_1_id = rows[result[-1]][0]
        tuple_0_already_clustered = tuple_0_id in clusters
        tuple_1_already_clustered = tuple_1_id in clusters

        if not tuple_0_already_clustered and not tuple_1_already_clustered:
            clusters[tuple_0_id] = cluster_id
            clusters[tuple_1_id] = cluster_id
            cluster_id += 1
        elif not tuple_0_already_clustered and tuple_1_already_clustered:
            clusters[tuple_0_id] = clusters[tuple_1_id]
        elif tuple_0_already_clustered and not tuple_1_already_clustered:
            clusters[tuple_1_id] = clusters[tuple_0_id]
        elif tuple_0_already_clustered and tuple_1_already_clustered:
            cluster_0 = clusters[tuple_0_id]
            cluster_1 = clusters[tuple_1_id]
            for record_id, cluster in clusters.items():
                if cluster == cluster_1:
                    clusters[record_id] = cluster_0

    # this is not very efficient.... but it works!
    for result in filter(lambda row: row[0] not in clusters, rows):
        clusters[result[0]] = cluster_id
        cluster_id += 1
    return clusters


def print_possible_duplicates(checked_metric, filtered_result, rows):
    for result in filtered_result:
        row1 = rows[result[-2]]
        row2 = rows[result[-1]]
        print('Possible Duplicate (d=' + str(result[checked_metric]) + '):')
        print(str(row1) + ' \n->\n' + str(row2))


def perform_comparisons():

    pool_size = 5
    pool = mp.Pool(pool_size)
    items = range(0, rows_to_deduplicate)
    for tuple_0_index in items:
        pool.apply_async(compare, (tuple_0_index,))
        # print(len(dict_res))
    pool.close()
    pool.join()


def compare(tuple_0_index):
    global comparisons_performed, dict_res
    try:
        for tuple_1_index in range(tuple_0_index + 1, rows_to_compare_to):
            tuple_0_string, tuple_1_string = stringify(tuple_0_index, tuple_1_index)
            distance = lv.ratio(tuple_0_string, tuple_1_string)
            key = (tuple_0_index, tuple_1_index)
            dict_res[key] = distance
            # The number of comparisons looked weird with multiprocessing,
            # I think the size of the dict (structure I used to avoid using comparisons_performed
            # as index, should reveal the number of tuples with different distances,
            # not necessarily the number of comparisons. That number might be useful for our report
            # but can be theoretically calculated (number of for-loops / number of threads).
        # print(len(dict_res))
    except:
        print('error comparing tuple')


def stringify(tuple_0, tuple_1):
    tuple_0_string = ''
    tuple_1_string = ''
    # this routine makes sure we don't compare two cells in which only one row has an entry, but the other
    # one doesn't index zero is intentionally left out, as it is the unique index
    for column in range(1, col_count):
        if (rows[tuple_0][column] != '') & (rows[tuple_1][column] != ''):
            val0 = rows[tuple_0][column].upper()
            val1 = rows[tuple_1][column].upper()

            # this adds weight to the names
            if column == 1 | column == 3:
                val0 *= name_weight
                val1 *= name_weight
            tuple_0_string += val0
            tuple_1_string += val1
    return tuple_0_string, tuple_1_string


def allocate_result_table(comparisons_needed, distance_measure_method_count):
    return alloc_2d_list(comparisons_needed, 2 + distance_measure_method_count)


def alloc_2d_list(rows, cols):
    return [[0 for x in range(cols)] for y in range(rows)]


def read_csv(file):
    with open(file) as csv_file:
        file_reader = csv.reader(csv_file)
        rows = []
        for row in file_reader:
            rows.append(row)

        rows = rows[1:]  # The first row is skipped as it contains only column names
        return rows


def print_dict():
    print(len(dict_res))
    for key, value in dict_res.items():
        print(key, value)

deduplicate("smalltest.csv", "out.csv")
