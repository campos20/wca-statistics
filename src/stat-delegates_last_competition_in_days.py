import datetime
from bisect import bisect_left
from build_page import build_results
from utils import *
import pandas as pd
import sys
from utils import get_delegates_list, iso2_country_name


def main():
    print("Getting delegate list")
    delegates_list = get_delegates_list()

    delegates_id = []
    delegates_name = []
    delegates_country = []
    delegates_last_competition_date = []
    delegates_last_competition_name = []
    day_diff = []

    for delegate in delegates_list:
        wca_id = delegate["wca_id"]
        name = delegate["name"]

        country_id = delegate["country_iso2"]

        i = bisect_left(delegates_name, name)

        delegates_id.insert(i, wca_id)
        delegates_name.insert(i, name)
        delegates_country.insert(i, country_id)
        # Who cares with the position of None
        delegates_last_competition_date.append(None)
        delegates_last_competition_name.append(None)
        day_diff.append(float("inf"))

    today = datetime.date.today()

    competitions = pd.read_csv(
        "WCA_export/WCA_export_Competitions.tsv", sep="\t")
    for index, row in competitions.iterrows():
        competition, year, month, day, delegates = row[[
            "id", "year", "month", "day", "wcaDelegate"]]

        competition_date = datetime.date(year, month, day)

        if competition_date > today:
            continue

        delegates = extract_delegate(delegates)

        for delegate in delegates:
            i = bisect_left(delegates_name, delegate)
            if i < len(delegates_name) and delegates_name[i] == delegate:
                if delegates_last_competition_date[i] == None or competition_date > delegates_last_competition_date[i]:
                    delegates_last_competition_date[i] = competition_date
                    delegates_last_competition_name[i] = competition
                    day_diff[i] = (today-competition_date).days

    out = {}
    out["title"] = "Last delegated competition in days"
    out["labels"] = ["#", "Days", "Delegate",
                     "Country", "Continent", "Last competition"]

    table = []

    prev = None
    pos = 1
    for days, wca_id, name, country, competition in sorted(zip(day_diff, delegates_id, delegates_name, delegates_country, delegates_last_competition_name))[::-1]:
        p = pos
        if days == prev:
            p = "-"
        if days != float("inf"):
            table.append([p, days, html_link_format(
                name, get_competitor_link(wca_id)), iso2_country_name(country), find_continent(iso2_country_name(country)), get_competition_html_link(competition)])
            pos += 1
        prev = days

    out["table"] = table

    build_results(out, sys.argv)


if __name__ == "__main__":
    main()
