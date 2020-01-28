from datetime import datetime, date
from bisect import bisect_left
from build_page import build_results
from utils import *
from Model import Competition
import pandas as pd
import re
import sys


def main():
    delegates_id = []
    delegates_name = []
    delegates_country = []
    delegates_competition_list = []
    delegates_distance_avg = []
    delegates_competition_count = []
    with open("database_out/delegates_list.txt") as f:
        for x in f:
            wca_id, name, region = x.split("\t")

            i = bisect_left(delegates_name, name)

            delegates_id.insert(i, wca_id)
            delegates_name.insert(i, name)
            delegates_country.insert(i, region)
            delegates_competition_list.insert(i, [])

    today = date.today()

    competitions = pd.read_csv(
        "WCA_export/WCA_export_Competitions.tsv", sep="\t")
    for _, row in competitions.iterrows():
        id, year, month, day, delegates, latitude, longitude, city, country = row[[
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

        delegates = extract_delegate(delegates)

        for delegate in delegates:
            index = bisect_left(delegates_name, delegate)
            # competition's delegate is no longer a delegate
            if index == len(delegates_name) or delegates_name[index] != delegate:
                continue
            delegates_competition_list[index].append(competition)

    for i in range(len(delegates_name)):
        for j in range(len(delegates_competition_list[i])):
            delegates_competition_list[i] = sorted(
                delegates_competition_list[i])

        total_distance = 0
        for j in range(1, len(delegates_competition_list[i])):
            # if delegates_competition_list[i][j].date < delegates_competition_list[i][j-1].date:
            #    raise "Not sorted"

            distance = delegates_competition_list[i][j].distance(
                delegates_competition_list[i][j-1])
            total_distance += distance
        number_of_competitions = len(delegates_competition_list[i])

        # avoid / 0
        delegates_distance_avg.append(1.0 *
                                      total_distance / max(1, number_of_competitions-1))
        delegates_competition_count.append(number_of_competitions)

    out = {}
    out["title"] = "Average distance by delegates in the past 365 days"
    out["labels"] = ["#", "Avg (km)", "Delegate",
                     "Country", "Number of competitions"]

    table = []

    prev = None
    pos = 1
    for avg, wca_id, name, country, count in sorted(zip(delegates_distance_avg, delegates_id, delegates_name, delegates_country, delegates_competition_count))[::-1]:
        p = pos
        result = "%.2f" % avg
        if result == prev:
            p = "-"
        table.append([p, result, html_link_format(
            name, get_competitor_link(wca_id)), iso2_country_name(country), count])
        pos += 1
        prev = result

    out["table"] = table
    out["explanation"] = "The Avg column is the average distance a delegate traveled from one competition to the next."

    build_results(out, sys.argv)


if __name__ == "__main__":
    main()
