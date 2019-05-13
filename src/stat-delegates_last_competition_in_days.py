from datetime import datetime, date
from bisect import bisect_left
from build_page import build_results
from utils import *
import pandas as pd
import re
import sys


def extract_delegate(line):
    out = []
    for x in re.findall("\[(.*?)\]", line):
        delegate = re.findall("\{(.*?)\}", x)
        delegate_name = delegate[0]
        out.append(delegate_name)
    return out


def main():
    delegates_id = []
    delegates_name = []
    delegates_country = []
    delegates_last_competition_date = []
    delegates_last_competition_name = []
    day_diff = []
    with open("database_out/delegates_list.txt") as f:
        for x in f:
            wca_id, name, region = x.split("\t")

            i = bisect_left(delegates_name, name)

            delegates_id.insert(i, wca_id)
            delegates_name.insert(i, name)
            delegates_country.insert(i, region)
            # Who cares with the position of None
            delegates_last_competition_date.append(None)
            delegates_last_competition_name.append(None)
            day_diff.append(float("inf"))

    today = datetime.today()

    competitions = pd.read_csv(
        "WCA_export/WCA_export_Competitions.tsv", sep="\t")
    for index, row in competitions.iterrows():
        competition, year, month, day, delegates = row[[
            "id", "year", "month", "day", "wcaDelegate"]]

        current_date = datetime(year, month, day)
        delegates = extract_delegate(delegates)

        for delegate in delegates:
            i = bisect_left(delegates_name, delegate)
            if i < len(delegates_name) and delegates_name[i] == delegate:
                if current_date <= today and (delegates_last_competition_date[i] == None or current_date > delegates_last_competition_date[i]):
                    delegates_last_competition_date[i] = current_date
                    delegates_last_competition_name[i] = competition
                    day_diff[i] = (today-current_date).days

        out = {}
        out["title"] = "Last delegated competition in days"
        out["labels"] = ["#", "Days", "Delegate", "Country", "Last competition"]

        table = []

    prev = None
    pos = 1
    for days, wca_id, name, country, competition in sorted(zip(day_diff, delegates_id, delegates_name, delegates_country, delegates_last_competition_name))[::-1]:
        p = pos
        if days == prev:
            p = "-"
        if days != float("inf"):
            table.append([p, days, html_link_format(
                name, get_competitor_link(wca_id)), country, get_competition_html_link(competition)])
            pos += 1

    out["table"] = table

    build_results(out, sys.argv)


if __name__ == "__main__":
    main()
