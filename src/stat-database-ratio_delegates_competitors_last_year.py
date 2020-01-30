import bisect
import csv
import datetime
import sys
from build_page import build_results
from utils import get_delegates_list, iso2_country_name


# This stat uses some data from the WCA API. So, make sure you run
# "setup.py" before running this and that


def ratio_competitors_delegates():

    days = 365

    countries_delegates = []
    number_of_delegates = []

    print("Getting delegate list")
    delegates_list = get_delegates_list()

    print("Counting how much delegates there exists for each country")
    for delegate in delegates_list:
        country = iso2_country_name(delegate["country_iso2"])

        # Results save as USA, so we replace here
        if country == "United States":
            country = "USA"

        i = bisect.bisect_left(countries_delegates, country)
        if i == len(countries_delegates) or countries_delegates[i] != country:
            # If the country does not exist yet, we add it and count 1 as number of delegate
            countries_delegates.insert(i, country)
            number_of_delegates.insert(i, 1)
        else:
            number_of_delegates[i] += 1

    competitors_last_year = []

    today = datetime.date.today()

    countries_persons = []
    competitors_id = []
    competitors_names = []

    tsvfile = open("WCA_export/WCA_export_Results_Ordered.tsv", "r")
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    next(tsvreader, None)
    for line in tsvreader:  # bisect here?
        year, month, day = map(int, [line[17], line[18], line[19]])
        date = datetime.date(year, month, day)
        if date + datetime.timedelta(days=days) >= today:
            person_name = line[6]
            person_id = line[7]
            country = line[8]

            i = bisect.bisect_left(countries_persons, country)
            if i == len(countries_persons) or countries_persons[i] != country:
                countries_persons.insert(i, country)
                competitors_id.insert(i, [])
                competitors_names.insert(i, [])

            j = bisect.bisect_left(competitors_id[i], person_id)
            if j == len(competitors_id[i]) or competitors_id[i][j] != person_id:
                competitors_id[i].insert(j, person_id)
                competitors_names[i].insert(j, person_name)

    ratios = []
    competitors_out = []
    for i in range(len(countries_delegates)):
        country = countries_delegates[i]
        delegates = number_of_delegates[i]

        j = bisect.bisect_left(countries_persons, country)
        number_of_competitors = len(competitors_id[j])
        competitors_out.append(number_of_competitors)

        ratio = 1.0*number_of_competitors/delegates  # 0 division is already avoided
        ratios.append(ratio)

    table = []
    c = 1
    prev = None
    for ratio, country, competitors, delegates in sorted(zip(ratios, countries_delegates, competitors_out, number_of_delegates))[::-1]:
        ratio_display = "%.2f" % ratio
        pos = c
        if ratio_display == prev:
            pos = "-"
        table.append([pos, ratio_display, country, competitors, delegates])
        c += 1
        prev = ratio_display

    out = {}
    out["title"] = "Ratio between number of active competitors in the last %s days and active delegates" % days
    out["labels"] = ["Pos", "Ratio", "Country",
                     "Active competitors", "Delegates"]
    out["explanation"] = 'That is: active competitors/delegates. It\'s the virtual number of different competitors each delegate had to handle in the past %s days (if everyone just competed in the home country). So, for the first position, %s, each one of the %s delegates had to deal with %s different competitors on average in the past %s days. <a href="stat-database-active_countries_with_no_delegates.html">Related</a>.' % (
        days, table[0][2], table[0][4], table[0][1], days)
    out["table"] = table
    return out


def main():
    args = sys.argv
    out = ratio_competitors_delegates()
    build_results(out, args)


if __name__ == "__main__":
    main()
