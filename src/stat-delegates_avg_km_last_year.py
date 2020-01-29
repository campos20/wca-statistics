from datetime import datetime, date
from bisect import bisect_left
from build_page import build_results
from utils import *
from Model import Competition, Competitor
import pandas as pd
import re
import sys


def main():
    delegates_list = get_delegates_list()
    delegates = list(map(delegate_json_2_delegate, delegates_list))

    # Sort delegates by name
    delegates.sort(key=lambda x: x.name)

    # Ordered list of delegates names for binary search
    delegates_ordered_names = list(map(lambda x: x.name, delegates))

    today = date.today()

    competitions = pd.read_csv(
        "WCA_export/WCA_export_Competitions.tsv", sep="\t")
    for _, row in competitions.iterrows():
        id, year, month, day, delegates_string, latitude, longitude, city, country = row[[
            "id", "year", "month", "day", "wcaDelegate", "latitude", "longitude", "cityName", "countryId"]]

        competition_date = date(year, month, day)
        if (today-competition_date).days > 365 or competition_date > today:
            continue

        # we exclude multiple countries competition
        # XA, XE...
        if len(country) == 2:
            continue

        # ideally, we would also avoid multiple cities competition, but this is not that feasible right now

        competition = Competition()
        competition.id = id
        competition.location = (latitude, longitude)
        competition.date = competition_date

        competition_delegates = extract_delegate(delegates_string)

        for delegate in competition_delegates:
            index = bisect_left(delegates_ordered_names, delegate)
            # competition's delegate is no longer a delegate
            if index == len(delegates_ordered_names) or delegates_ordered_names[index] != delegate:
                continue
            delegates[index].competition_list.append(competition)

    for delegate in delegates:

        # Sort competitions by date
        delegate.competition_list.sort()

        total_distance = 0
        for j in range(1, len(delegate.competition_list)):
            if delegate.competition_list[j].date < delegate.competition_list[j-1].date:
                raise "Not sorted"

            distance = delegate.competition_list[j].distance(
                delegate.competition_list[j-1])
            total_distance += distance
        number_of_competitions = len(delegate.competition_list)

        # avoid / 0
        delegate.avg = total_distance / max(1, number_of_competitions-1)

    # Sort delegates by distance
    delegates.sort(key=lambda x: x.avg)

    out = {}
    out["title"] = "Average distance by delegates in the past 365 days"
    out["labels"] = ["#", "Avg (km)", "Delegate",
                     "Country", "Number of competitions"]

    table = []

    prev = None
    pos = 1
    for delegate in delegates[::-1]:
        p = pos
        result = "%.2f" % delegate.avg
        if result == prev:
            p = "-"
        table.append([p, result, html_link_format(
            delegate.name, delegate.url), delegate.country, len(delegate.competition_list)])
        pos += 1
        prev = result

    out["table"] = table
    out["explanation"] = "The Avg column is the average distance a delegate traveled from one competition to the next."

    build_results(out, sys.argv)


def delegate_json_2_delegate(delegate_json):
    wca_id = delegate_json["wca_id"]
    name = delegate_json["name"]
    country_id = delegate_json["country_iso2"]
    url = delegate_json["url"]

    delegate = Competitor()

    delegate.wca_id = wca_id
    delegate.name = name
    delegate.country = iso2_country_name(country_id)
    delegate.url = url
    delegate.competition_list = []

    # Custom attribute
    delegate.avg = None

    return delegate


if __name__ == "__main__":
    main()
