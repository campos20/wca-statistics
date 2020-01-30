import bisect
import csv
import datetime
import sys
from build_page import build_results
from utils import get_delegates_list, iso2_country_name

# This is basically the NA countries from stat-database-ratio_delegates_competitors_last_year.py


def no_delegates():
    days = 365

    print("Getting delegate list")
    delegates_list = get_delegates_list()

    countries_delegates = list(map(iso2_country_name, list(
        set(map(lambda x: x["country_iso2"], delegates_list)))))
    print("Number of countries with at least 1 delegate: %s" %
          len(countries_delegates))

    countries_delegates.sort()

    # Competitors from United States are recorded as USA. This messes by saying that USA has no delegates.
    # We replace 'United States' with USA.
    usa_long_name = "United States"
    j = bisect.bisect_left(countries_delegates, usa_long_name)
    if j < len(countries_delegates) and countries_delegates[j] == usa_long_name:
        countries_delegates[j] = "USA"
        countries_delegates.sort()

    today = datetime.date.today()

    active_countries_competitors_list = []

    print("Searching the results for active countries")
    active_countries = []
    tsvfile = open("WCA_export/WCA_export_Results_Ordered.tsv", "r")
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    next(tsvreader, None)  # skip header
    for line in tsvreader:  # bisect here?
        year, month, day = map(int, [line[17], line[18], line[19]])
        date = datetime.date(year, month, day)
        if date + datetime.timedelta(days=days) < today:
            continue

        wca_id = line[7]
        country = line[8]

        i = bisect.bisect_left(active_countries, country)

        # New active country found
        if i == len(active_countries) or active_countries[i] != country:
            active_countries.insert(i, country)
            active_countries_competitors_list.insert(i, [wca_id])
        else:
            # If the country already exists,
            j = bisect.bisect_left(
                active_countries_competitors_list[i], wca_id)
            if j == len(active_countries_competitors_list[i]) or active_countries_competitors_list[i][j] != wca_id:
                active_countries_competitors_list[i].insert(j, wca_id)

    print("Number of active countries: %s" % len(active_countries))

    print("Searching for active countries with no delegates")
    table = []
    no_delegates_country = []
    no_delegates_country_competitor_count = []
    for i in range(len(active_countries)):
        country = active_countries[i]
        j = bisect.bisect_left(countries_delegates, country)

        if j == len(countries_delegates) or countries_delegates[j] != country:
            no_delegates_country.append(country)
            no_delegates_country_competitor_count.append(
                len(active_countries_competitors_list[i]))

    print("Building table")
    c = 1
    prev = None
    for competitors, country in sorted(zip(no_delegates_country_competitor_count, no_delegates_country))[::-1]:
        pos = c
        if competitors == prev:
            pos = "-"
        table.append([pos, competitors, country])
        c += 1
        prev = competitors

    out = {}
    out["title"] = "Active countries with no delegates in the last %s days" % days
    out["labels"] = ["Pos", "Active competitors", "Country"]
    out["explanation"] = 'A country is considered active here if a competitor from that country has competed in the past %s days. <a href="stat-database-ratio_delegates_competitors_last_year.html">Related</a>.' % days
    out["table"] = table

    return out


def main():
    args = sys.argv

    print("Active countries with no delegates")
    out = no_delegates()

    print("Building page")
    build_results(out, args)


if __name__ == "__main__":
    main()
