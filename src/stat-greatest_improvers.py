import bisect
import csv
import sys

from build_page import build_results
from utils import *

limit = 50
n = 100


def best_improvers():

    with open('WCA_export/WCA_export_Results_Ordered.tsv') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')

        prev_competition = None
        prev_event = None

        result_wca_id = []
        result_names = []
        result_best_single = []
        result_average = []
        result_total = []
        result_country = []

        wca_ids = []
        singles = []
        averages = []
        ratio = []

        skip_header = True

        for line in tsvin:
            if skip_header:
                skip_header = False
                continue

            current_competition = line[0]
            current_event = line[1]

            wca_id = line[7]
            best = line[4]
            avg = line[5]
            name = line[6]

            if current_competition != prev_competition or prev_event != current_event:
                wca_ids = []
                singles = []
                averages = []

            # index in the current competition / event
            index = bisect.bisect_left(wca_ids, wca_id)

            if index == len(wca_ids) or wca_ids[index] != wca_id:

                wca_ids.insert(index, wca_id)
                singles.insert(index, [])
                averages.insert(index, [])

            singles[index].append(int(best))
            averages[index].append(int(avg))

            if len(singles[index]) > 1:
                # index for every competitor
                general_index = bisect.bisect_left(result_wca_id, wca_id)

                if general_index == len(result_wca_id) or result_wca_id[general_index] != wca_id:
                    result_wca_id.insert(general_index, wca_id)
                    result_names.insert(general_index, name)
                    result_best_single.insert(general_index, 0)
                    result_average.insert(general_index, 0)
                    result_total.insert(general_index, 0)
                    result_country.insert(general_index, line[8])

                if singles[index][-1] > 0 and singles[index][-1] <= singles[index][-2]:
                    result_best_single[general_index] += 1

                if averages[index][-1] > 0 and averages[index][-1] <= averages[index][-2]:
                    result_average[general_index] += 1

                result_total[general_index] += 1

            prev_competition = current_competition
            prev_event = current_event

    table = []

    for i in range(len(result_wca_id)):
        ratio.append(100.0 * result_best_single[i] / result_total[i])

    count = 1
    prev = None
    for r, name, country, single,  avg, tt, wca_id in sorted(zip(ratio, result_names, result_country, result_best_single, result_average, result_total, result_wca_id))[::-1]:
        if tt < limit:
            continue

        result = "%.2f%%" % r

        if prev != result and count > n:
            break

        pos = "-" if prev == result else count

        prev = result

        # table.append([pos, name, country, "%.2f%%" % r, single, avg, tt])
        table.append([pos, name, country, "%.2f%%" % r, single, tt])
        count += 1

    out = {}
    out["title"] = "Result better than the previous in a competition"
    out["explanation"] = "Competitors who got a better single in the next round when compared to the previous. Limited to competitors with at least %s possible results" % limit
    out["table"] = table
    out["labels"] = ["#", "Name", "Country",
                     "Ratio", "Improvements", "Total"]
    return out


def main():

    args = sys.argv
    out = best_improvers()

    build_results(out, args)


main()
