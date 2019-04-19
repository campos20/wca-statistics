import pandas as pd
from datetime import date

championships = pd.read_csv("WCA_export/WCA_export_championships.tsv", sep="\t")
competitions = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep="\t")
countries = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")
results = pd.read_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep="\t")

def get_competition_date(competition):
    year, month, day = competitions[competitions["id"] == competition][["year", "month", "day"]].values[0]
    return date(year, month, day)

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

def get_regional_champion(competition, region, event):
    return results[(results["competitionId"] == competition) & (results["eventId"] == event) & (results["personCountryId"] == region)][["personName", "personId"]].values[-1]

def iso_2_id(region_iso):
    return countries[countries["iso2"] == region_iso]["id"].values[0]

def get_next_competition(person_id, current_competition, event):
    idx = results[(results["competitionId"] == current_competition) & (results["eventId"] == event)].index.values[-1]
    df = results[(results.index > idx) & (results["eventId"] == event) & (results["personId"] == person_id)]["competitionId"]
    if df.empty:
        return
    return df.values[0]

def walk_path(region_iso, event, start_date = None, region = None, championship = None, champion = None, champion_id = None):

    if region == None:
        region = iso_2_id(region_iso)

    if championship == None:
        championship, start_date = get_next_championship_with_date(region_iso, start_date)
    
    if champion_id == None: # TODO join this within the else
        champion, champion_id = get_regional_champion(championship, region, event)
        print("New champion:", champion, champion_id, championship)
    else:
        next_competition = get_next_competition(champion_id, championship, event)
        if next_competition == None:
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
    event = "333bf"
    walk_path(region_iso, event)

def main():
    unofficial_official()

if __name__ == '__main__':
    main()
