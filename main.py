import Levenshtein as lv
import csv
import time


def deduplicate(file):
    rows = read_csv(file)

    approaches = ['distance', 'jaro', 'jaro_winkler', 'ratio', 'seqratio', 'setratio']
    distance_measure_method_count = len(approaches)

    row_count = len(rows)
    col_count = len(rows[0])

    # The following variables are just for testing purposes
    # rows_to_deduplicate = 10
    # rows_to_compare_to = 20000
    rows_to_deduplicate = row_count
    rows_to_compare_to = row_count

    name_weight = 3

    comparisons_needed = int(rows_to_compare_to * rows_to_deduplicate
                             - (rows_to_deduplicate * rows_to_deduplicate - rows_to_deduplicate) / 2)

    res = allocate_result_table(comparisons_needed, distance_measure_method_count)

    start_time = time.time()

    comparisons_performed = perform_comparisons(col_count, name_weight, res, rows,
                                                rows_to_compare_to, rows_to_deduplicate)
    # this makes sure the result set does not have more entries than needed.
    # Theoretically this is unnecessary, but its neat for testing purposes
    res = res[:(comparisons_performed - 1)]

    elapsed_time = time.time() - start_time

    checked_metric = 3
    threshold = 0.85
    filtered_result = list(filter(lambda r: r[checked_metric] > threshold, res))

    print_possible_duplicates(checked_metric, filtered_result, rows)


    clusters = []
    clusterID = 1
    for result in filtered_result:
        row1 = rows[result[-2]]
        row2 = rows[result[-1]]
        clusters.append([clusterID, row1[0]])
        clusters.append([clusterID, row2[0]])
        clusterID += 1

    clusterCol1 = [row[1] for row in clusters]
    for comparisons_performed in range(1, len(clusterCol1)):
        try:
            foundIndex = clusterCol1.index(clusterCol1[comparisons_performed], 0, comparisons_performed)  # the ID is already in a different cluster!
            clusterToBeMerged = clusters[foundIndex][0]
            myCluster = clusters[comparisons_performed][0]

            for row in clusters:
                if row[0] == myCluster:
                    row[0] = clusterToBeMerged
        except ValueError:  # not found
            continue

    print('clusters:')
    for row in clusters:
        print(str(row))

    print('Elapsed Time: {time} seconds '.format(time=str(elapsed_time)))


def print_possible_duplicates(checked_metric, filtered_result, rows):
    for result in filtered_result:
        row1 = rows[result[-2]]
        row2 = rows[result[-1]]
        print('Possible Duplicate (d=' + str(result[checked_metric]) + '):')
        print(str(row1) + ' \n->\n' + str(row2))


def perform_comparisons(col_count, name_weight, res, rows, rows_to_compare_to, rows_to_deduplicate):
    comparisons_performed = 0
    for tuple_0_index in range(0, rows_to_deduplicate):
        for tuple_1_index in range(tuple_0_index + 1, rows_to_compare_to):
            tuple_0_string, tuple_1_string = stringify(col_count, name_weight, rows, tuple_0_index, tuple_1_index)

            res[comparisons_performed][0] = lv.distance(tuple_0_string, tuple_1_string)
            res[comparisons_performed][1] = lv.jaro(tuple_0_string, tuple_1_string)
            res[comparisons_performed][2] = lv.jaro_winkler(tuple_0_string, tuple_1_string)
            res[comparisons_performed][3] = lv.ratio(tuple_0_string, tuple_1_string)
            res[comparisons_performed][4] = lv.seqratio(tuple_0_string, tuple_1_string)
            res[comparisons_performed][5] = lv.setratio(tuple_0_string, tuple_1_string)
            res[comparisons_performed][-2] = tuple_0_index
            res[comparisons_performed][-1] = tuple_1_index
            comparisons_performed += 1
            if comparisons_performed % 1000 == 0:
                print(comparisons_performed)

    return comparisons_performed


def stringify(col_count, name_weight, rows, tuple_0, tuple_1):
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


def allocate_result_table(comparisons_needed, distanceMeasureMethodCount):
    return [[0 for x in range(2 + distanceMeasureMethodCount)] for y in range(comparisons_needed)]

def read_csv(file):
    with open(file) as csv_file:
        file_reader = csv.reader(csv_file)
        rows = []
        for row in file_reader:
            rows.append(row)

        rows = rows[1:]  # The first row is skipped as it contains only column names
        return rows

deduplicate("smalltest.csv")
