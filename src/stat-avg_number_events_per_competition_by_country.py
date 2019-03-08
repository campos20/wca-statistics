import csv, sys
from utils import *
import pandas as pd
from build_page import build_results

def avg_events():
	
	country_list = []
	event_list = []
	discard = 1
	
	data = pd.read_csv('WCA_export/WCA_export_Competitions.tsv', sep='\t')
	for country, events in zip(data["countryId"], data["eventSpecs"]):
		   
		if country not in country_list:
			country_list.append(country)
			event_list.append([])
		   
		i = country_list.index(country)
		   
		events = events.split()
		event_list[i].append(len(events))

	for x in event_list:
		avg_list = map(avg, event_list)
	   
	count = 1
	prev = None
	table = []
	for (x, y, z) in sorted(zip(avg_list, country_list, event_list))[::-1]:
		if len(z)>discard:
			pos = "-"
			if prev != "%.2f"%x:
				pos = count
			table.append([pos, ("%.2f"%x).zfill(5), y])
			count += 1
			prev = "%.2f"%x

	out = {}
	out["title"] = "Avg number of events in a competition for each country"
	out["labels"] = ["#", "Avg", "Country"]
	out["table"] = table
	
	return out

def main():
	stat = avg_events()
	args = sys.argv
	build_results(stat, args)
	
main()
