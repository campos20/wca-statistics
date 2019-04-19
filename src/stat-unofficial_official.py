import pandas as pd
from datetime import date

championships = pd.read_csv("WCA_export/WCA_export_championships.tsv", sep="\t")
competitions = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep="\t")

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


def unofficial_official():
	print(get_next_championship_with_date("US"))

def main():
	unofficial_official()

if __name__ == '__main__':
	main()