import pandas as pd

championships = pd.read_csv("WCA_export/WCA_export_championships.tsv", sep="\t")
competitions = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep="\t")
countries = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")

results = pd.read_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep="\t")
results = results.drop(columns=["value1", "value2", "value3", "value4", "value5", "regionalSingleRecord", "regionalAverageRecord", "average"]) # drop some values
results["date"] = results['date'].astype('datetime64[ns]')
last_date = results["date"].values[-1]

def get_competition_date(competition):
    year, month, day = competitions[competitions["id"] == competition][["year", "month", "day"]].values[0]
    return pd.Timestamp(year, month, day)

# TODO. Fix this. Put if to use start_date. Also, this must be event aware.
def get_next_championship_with_date(region, start_date = None):

    dt = None
    championship = None

    for index, row in championships[championships["championship_type"] == region].iterrows():

        comp = row["competition_id"]
        comp_date = get_competition_date(comp)

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

    if championship == None:
        championship, start_date = get_next_championship_with_date(region_iso, start_date)
    
    if champion_id == None: # TODO join this within the else
        champion, champion_id = get_regional_champion(championship, region, event)
        print("New champion:", champion, champion_id, championship)
    else:
        prev_date = start_date
        next_competition, start_date = get_next_competition_with_date(champion_id, start_date, event)
        if next_competition == None:
            if prev_date + pd.DateOffset(years = 1) <= last_date:
                # Competitor did not compete for 1 year
                champion, champion_id = look_back(champion_id, prev_date, event, region)
                if champion_id == None:
                    championship, start_date = get_next_championship_with_date(region_iso, start_date)
                    if championship == None:
                        print("Terminating")
                        return
                else:
                    print("Title fall 2:", champion, champion_id, championship)
                    walk_path(region_iso, event, prev_date, region, championship, champion, champion_id)
                    return
            return
        regional_winner, regional_winner_id = get_regional_champion(next_competition, region, event)

        if regional_winner_id != champion_id:
            print("New champion:", regional_winner, regional_winner_id, next_competition)

        championship = next_competition
        champion = regional_winner
        champion_id = regional_winner_id
    
    walk_path(region_iso, event, start_date, region, championship, champion, champion_id)

def unofficial_official():

    region_iso = "US"
    event = "444"
    walk_path(region_iso, event)

def main():
    unofficial_official()

if __name__ == '__main__':
    main()
