import Levenshtein as lv
import csv
import time

rows_to_skip = set()

last_name_weight = 2
first_name_weight = 5
ssn_weight = 2


def deduplicate(infile, outfile):
    rows = read_csv(infile)

    row_count = len(rows)
    col_count = len(rows[0])

    # The following variables are just for testing purposes
    # rows_to_deduplicate = 10
    # rows_to_compare_to = 20000
    rows_to_deduplicate_start = int(0)
    rows_to_deduplicate_end = rows_to_deduplicate_start + int(100)
    for i in range(1, 100):
        rows_to_compare_to = row_count

        name_weight = 5

        start_time = time.time()

        res = perform_comparisons(col_count, name_weight, rows,
                                                rows_to_compare_to, rows_to_deduplicate_start, rows_to_deduplicate_end)

        elapsed_time = time.time() - start_time

        threshold = 0.85

        duplicates = list(filter(lambda r: r[0] > threshold, res))

        print_possible_duplicates(0, duplicates, rows)

        clusters = create_duplicate_clusters(duplicates, rows)

        sorted_clusters = to_sorted_cluster_list(clusters)

        print_clusters(sorted_clusters)

        write_clusters_to_file(outfile + str(i), sorted_clusters)

        rows_to_deduplicate_start = rows_to_deduplicate_end
        rows_to_deduplicate_end += 100

        print('Elapsed Time: {time} seconds '.format(time=str(elapsed_time)))
        del res
        del duplicates
        del clusters
        del sorted_clusters
        gc.collect()


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
    #for result in filter(lambda row: row[0] not in clusters, rows):
    #    clusters[result[0]] = cluster_id
    #    cluster_id += 1
    return clusters


def print_possible_duplicates(checked_metric, filtered_result, rows):
    for result in filtered_result:
        row1 = rows[result[-2]]
        row2 = rows[result[-1]]
        print('Possible Duplicate (d=' + str(result[checked_metric]) + '):')
        print(str(row1) + ' \n->\n' + str(row2))


def perform_comparisons(col_count, rows, rows_to_compare_to, rows_to_deduplicate_start, rows_to_deduplicate_end):
    res = []
    i = 0
    for tuple_0_index in range(rows_to_deduplicate_start, rows_to_deduplicate_end):
        if tuple_0_index in rows_to_skip:
            continue

        for tuple_1_index in range(tuple_0_index + 1, rows_to_compare_to):
            if tuple_1_index in rows_to_skip:
                continue

            tuple_0_string, tuple_1_string = stringify(col_count, rows, tuple_0_index, tuple_1_index)

            distance = lv.ratio(tuple_0_string, tuple_1_string)
            res.append([distance, tuple_0_index, tuple_1_index])

            if distance > 0.9:
                rows_to_skip.add(tuple_1_index)

            i += 1
            if i % 100000 == 0:
                print(i)
    return res


def stringify(col_count, rows, tuple_0, tuple_1):
    tuple_0_string = ''
    tuple_1_string = ''
    # this routine makes sure we don't compare two cells in which only one row has an entry, but the other
    # one doesn't index zero is intentionally left out, as it is the unique index
    for column in range(1, col_count):
        if (rows[tuple_0][column] != '') & (rows[tuple_1][column] != ''):
            val0 = rows[tuple_0][column].upper()
            val1 = rows[tuple_1][column].upper()

            # this adds weight to the names
            if column == 1:
                val0 *= first_name_weight
                val1 *= first_name_weight
            elif column == 3:
                val0 *= last_name_weight
                val1 *= last_name_weight
            elif column == 10:
                val0 *= ssn_weight
                val1 *= ssn_weight

            tuple_0_string += val0
            tuple_1_string += val1
    return tuple_0_string, tuple_1_string


def allocate_result_table(comparisons_needed,):
    return alloc_2d_list(comparisons_needed, 3)


def alloc_2d_list(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def read_csv(file):
    with open(file) as csv_file:
        file_reader = csv.reader(csv_file)
        rows = []
        for row in file_reader:
            rows.append(row)

        rows = rows[1:]  # The first row is skipped as it contains only column names
        return rows

deduplicate("smallInput.csv", "out.csv")
