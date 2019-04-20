import pandas as pd
from utils import get_set_wca_events
championships = pd.read_csv("WCA_export/WCA_export_championships.tsv", sep="\t")
competitions = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep="\t")
countries = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")

results = pd.read_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep="\t")
results = results.drop(columns=["value1", "value2", "value3", "value4", "value5", "regionalSingleRecord", "regionalAverageRecord", "average"]) # drop some values
results["date"] = results['date'].astype('datetime64[ns]')
last_date = results["date"].values[-1]

final = {}

def get_competition_date(competition):
    year, month, day = competitions[competitions["id"] == competition][["year", "month", "day"]].values[0]
    return pd.Timestamp(year, month, day)

def get_events(competition_id):
    events = competitions[competitions["id"] == competition_id]["eventSpecs"].values[0]
    return events.split()

# TODO. Fix this. Put if to use start_date. Also, this must be event aware.
def get_next_championship_with_date(region, event, start_date = None):

    championship = None
    dt = None

    for index, row in championships[championships["championship_type"] == region].iterrows():

        comp = row["competition_id"]
        comp_date = get_competition_date(comp)

        events = get_events(comp)
        if event in events:

            if start_date == None:
                if dt == None or comp_date < dt:
                    championship = comp
                    dt = comp_date
            else:
                if comp_date > start_date:
                    if dt == None or comp_date < dt:
                        championship = comp
                        dt = comp_date

    return championship, dt

def get_regional_champion(competition, region, event, blacklist = []):
    df = results[(results["competitionId"] == competition) & (results["eventId"] == event) & (results["personCountryId"] == region)][["personName", "personId"]]
    df = df.reindex(index = df.index[::-1])
    for index, row in df.iterrows():
        champion, champion_id = row[["personName", "personId"]]
        if champion_id not in blacklist:
            return champion, champion_id
    return None, None

def iso_2_id(region_iso):
    return countries[countries["iso2"] == region_iso]["id"].values[0]

def get_next_competition_with_date(person_id, date, event):
    df = results[(results["date"] > date) & (results["date"] <= date + pd.DateOffset(years = 1)) & (results["eventId"] == event) & (results["personId"] == person_id)][["competitionId", "date"]]

    if df.empty:
        return None, None
    return df.values[0]

def get_previous_competitions(person_id, date, event):
    out = []
    for competition in results[(results["date"] <= date) & (results["date"] + pd.DateOffset(years = 1) >= date) & (results["eventId"] == event) & (results["personId"] == person_id)]["competitionId"].values:
        if len(out) == 0 or out[-1] != competition:
            out.append(competition)
    return out

def look_back(person_id, date, event, region):
    competitions = get_previous_competitions(person_id, date, event)
    blacklist = [person_id]
    for competition in competitions[::-1]:
        champion, champion_id = get_regional_champion(competition, region, event, blacklist)
        if champion_id != None:
            next_competition, next_date = get_next_competition_with_date(champion_id, date, event)
            if next_competition == None: # In this case, the next champion also has gone idle.
                blacklist.append(champion_id)
            else:
                return champion, champion_id
    return None, None

def walk_path(region_iso, event, start_date = None, region = None, championship = None, champion = None, champion_id = None):

    if region == None:
        region = iso_2_id(region_iso)
        final[region_iso]["region"] = region

    if championship == None:
        championship, start_date = get_next_championship_with_date(region_iso, event, start_date)
    
    if champion_id == None: # TODO join this within the else
        champion, champion_id = get_regional_champion(championship, region, event)
        final[region_iso][event].append([champion, champion_id, championship, "New"])
    else:
        prev_date = start_date
        next_competition, start_date = get_next_competition_with_date(champion_id, start_date, event)
        if next_competition == None:
            if prev_date + pd.DateOffset(years = 1) <= last_date:
                # Competitor did not compete for 1 year
                champion, champion_id = look_back(champion_id, prev_date, event, region)
                if champion_id == None:
                    championship, start_date = get_next_championship_with_date(region_iso, event, start_date)
                    if championship == None:
                        print("Terminating")
                        return
                    else:
                        print("Fresh new start")
                        # Fresh new start logic goes here
                        return
                    return
                else:
                    final[region_iso][event].append([champion, champion_id, championship, "Inactive"])
                    walk_path(region_iso, event, prev_date, region, championship, champion, champion_id)
                    return
            return
        regional_winner, regional_winner_id = get_regional_champion(next_competition, region, event)

        if regional_winner_id != champion_id:
            final[region_iso][event].append([regional_winner, regional_winner_id, next_competition, "New"])

        championship = next_competition
        champion = regional_winner
        champion_id = regional_winner_id
    
    walk_path(region_iso, event, start_date, region, championship, champion, champion_id)

def unofficial_official():

    region_iso = "BR"
    final[region_iso] = {}

    for event in sorted(list(get_set_wca_events())):

        final[region_iso][event] = []

        walk_path(region_iso, event)

        print(region_iso, final[region_iso]["region"])
        print(event)
        for x in final[region_iso][event]:
            print(x)

def main():
    unofficial_official()

if __name__ == '__main__':
    main()
