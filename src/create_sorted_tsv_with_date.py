import pandas as pd
import bisect
from datetime import date

def main():
	"""This sorts (date, competition, round) WCA_export_Results and creates a new tsv so it can be reused for other programs."""

	data_results = pd.read_csv('WCA_export/WCA_export_Results.tsv', sep='\t')
	data_competition = pd.read_csv('WCA_export/WCA_export_Competitions.tsv', sep='\t')
	
	# WCA sorts WCA_export_Competitions based on not case sensitive competitionId
	# This messes with bisect, so we create a competitionId list all caps
	competition_id_competition_all_caps =[x.upper() for x in data_competition["id"]]
	
	dates = []
	
	prev = None
	year = None
	month = None
	day = None
	
	for competitionId in data_results["competitionId"]:
		if competitionId != prev:
			i = bisect.bisect_left(competition_id_competition_all_caps, competitionId.upper()) # we match competitionId.upper here
			year = (data_competition["year"])[i]
			month = (data_competition["month"])[i]
			day = (data_competition["day"])[i]
		dates.append(date(year, month, day))
		prev = competitionId
	
	data_results["date"] = dates
	data_results['date'].astype('datetime64[ns]')
	print(data_results["date"])

	del data_competition, competition_id_competition_all_caps
	
	# this assumes that this is the possible order of roundTypeId
	# ['0', '1', '2', '3', 'b', 'c', 'd', 'e', 'f', 'h']
	# I'm not quite sure about this just yet
	data_results.sort_values(by=["date", "competitionId", "eventId", "roundTypeId", "pos"], ascending=[True, True, True, True, False], inplace=True)
	
	data_results.to_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep='\t', encoding='utf-8', index=False)

main()

