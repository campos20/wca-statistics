import csv, sys
from build_page import build_results
from utils import *
from datetime import date

def get_comp_with_n_days(days):

	limit = 12
	with open('WCA_export/WCA_export_Competitions.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		name = []
		country = []
		events_number = []
		
		header = True
		
		for line in tsvin:

			events = len(line[10].split())
			if events <= limit or header:
				header = False
				continue
			
			year = int(line[5])
			month = int(line[6])
			day = int(line[7])
			end_month = int(line[8])
			end_day = int(line[9])
			
			d0 = date(year, month, day)
			d1 = date(year, end_month, end_day)
			
			delta = d1 - d0
			
			if abs(delta.days)+1 == days:
				name.append(line[0])
				country.append(line[3])
				events_number.append(events)
	
	out = {}
	out["title"] = "1 day competition with lots of events"
	out["labels"] = ["Number of events", "Competition", "Country"]
	
	table = []
	for x, y, z in sorted(zip(events_number, name, country))[::-1]:
		link = "https://www.worldcubeassociation.org/competitions/%s"%y
		table.append([x, html_link_format(y, link), z])
	out["table"] = table
	
	return out

def main():

	args = sys.argv
	n = 0

	try:
		n = int(args[1])
	except:
		n = 1 # we assume n=1
	
	stat = get_comp_with_n_days(n)
	build_results(stat, args)
	
main()
