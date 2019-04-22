import bisect, json, datetime, sys
import pandas as pd
from utils import get_set_wca_events

championships = pd.read_csv("WCA_export/WCA_export_championships.tsv", sep="\t")
competitions = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep="\t")
countries = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")

results = pd.read_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep="\t")
results = results.drop(columns=["value1", "value2", "value3", "value4", "value5", "regionalSingleRecord", "regionalAverageRecord", "average"]) # drop some values
results["date"] = results['date'].astype('datetime64[ns]')
last_date = results["date"].values[-1]

class Champion():
    """Hold info about champions."""
    def __init__(self, champion_id, champion_name, competition, date):
        self.champion_id = champion_id
        self.champion_name = champion_name
        self.competition = competition
        self.date = date

    def __lt__(self, other):
        if self.date == other.date:
            return self.champion_name < other.champion_name
        else:
            return self.date < other.date

    def __eq__(self, other):
        return self.champion_id == other.champion_id and self.competition == other.competition

    def __str__(self):
        return str([self.champion_id, self.champion_name, self.competition])

class Champions_Holder():

    def __init__(self):
        self.champions = []

    def __str__(self):
        return str(self.champions)
    
    # This function also returns a status.
    # True means that this path has already been checked, no need to proceed.
    def add_champion(self, champion):
        i = bisect.bisect_left(self.champions, champion)
        if i < len(self.champions) and self.champions[i] == champion:
            return False
        else:
            self.champions.insert(i, champion)
            return True

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
    df = results[(results["competitionId"] == competition) & (results["eventId"] == event) & (results["personCountryId"] == region) & (results["best"] > 0) & (~results["personId"].isin(blacklist))]
    if df.empty:
        return []

    # In case competition had multiple rounds, we take just the last one.
    # Eventually, this will go back to previous rounds if blacklist goes to crowded
    final_round = df["roundTypeId"].values[-1]

    winning_pos = df[df["roundTypeId"] == final_round]["pos"].values[-1] # Helps in ties.

    winners_list = df[(df["pos"] == winning_pos) & (df["roundTypeId"] == final_round)][["personId", "personName"]].values
    return winners_list

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

def walk_path(region_iso, region, event, date = None, competition = None, champion_id = None, champion = None, blacklist = []):

    if competition == None:
        competition, date = get_next_championship_with_date(region_iso, event, date)
        if competition == None:
            return
    
    winners = get_regional_champion(competition, region, event, blacklist)
    for winner in winners:

        winner_id, winner_name = winner
        if winner_id != champion_id:
            new_champion = Champion(winner_id, winner_name, competition, date)
            status = final[region][event].add_champion(new_champion) # Add and return status
            if not status:
                return # In this case, this path has already been checked.
        champion_id, champion = winner_id, winner
        
        prev_competition = competition
        prev_date = date
        
        competition, date = get_next_competition_with_date(champion_id, date, event)
        
        if competition == None:
            if prev_date + pd.DateOffset(years = 1) > last_date:
                return
            blacklist.append(champion_id)
            competition = prev_competition
            date = prev_date

        walk_path(region_iso, region, event, date, competition, champion_id, champion, blacklist)

def get_all_regions_with_nats():
    isos = championships[championships["championship_type"].str.len() == 2]["championship_type"].values
    return sorted(list(set(isos)))

final = {}
def unofficial_official():

    for region_iso in get_all_regions_with_nats():

        region = iso_2_id(region_iso)
        print(region)
        final[region] = {}

        for event in sorted(list(get_set_wca_events())):
            print(event)
        
            final[region][event] = Champions_Holder()
            walk_path(region_iso, region, event)
            print()

        print()


    # It looks like pd.Timestamp is not serializable.
    # That's why we use that if.
    out = "var data = "+json.dumps(final, default = lambda x: str(x) if isinstance(x, pd.Timestamp) else x.__dict__, indent = 2)
    out += ";"
    create_out_data(out)
    create_page()

def create_out_data(out):
    with open("pages/unofficial_official_data.js", "w", encoding="utf8") as fout:
        fout.write(out)

def create_page():

    file_name = "stat-unofficial_official.html"
    for x in sys.argv: # Double check
        x = x.split("/")[-1].split(".")[0]
        file_name = x+".html"

    # This part copies script from src to pages.
    # Pages gets flushed, so this copy is helpful.
    script = open("src/unofficial_official.js", "r", encoding="utf8").read()
    with open("pages/unofficial_official.js", "w", encoding="utf8") as fout:
        fout.write(script)

    title = "Unofficial official champion"
    explanation = ""

    header = open("template/header.html", "r", encoding="utf8").read()%title
    nav_bar = open("template/nav_bar.html", "r", encoding="utf8").read()
    footer = open("template/footer.html", "r", encoding="utf8").read()%file_name
    closing = open("template/closing.html", "r", encoding="utf8").read()

    content = '<script src="unofficial_official_data.js"></script>\n'
    content += '<script src="unofficial_official.js"></script>'

    page = open("template/stat.html", "r", encoding="utf8").read()%(header, nav_bar, title, explanation, content, footer, closing)
    with open("pages/%s"%file_name, "w", encoding="utf8") as fout:
        fout.write(page)

def main():
    unofficial_official()

if __name__ == '__main__':
    main()