from datetime import date
import csv, sys
from build_page import build_page

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
			if events > limit or header:
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
	
	out = ["%s days competition with few events"%days]
	out.append(["Number of events", "Competition", "Country"])
	
	count = 0
	previous = 0
	for x, y, z in sorted(zip(events_number, name, country)):
		out.append([x, '<a href="https://www.worldcubeassociation.org/competitions/%s">%s</a>'%(y,y), z])
	return out

def main():
	"""Usage:
	"""

	args = sys.argv
	n = 0

	try:
		n = int(args[1])
	except:
		n = 3 # we assume n=1
		
	page = build_page(get_comp_with_n_days(n))	
	
	with open("pages/3_days_competitions_with_few_events.html", "w", encoding="utf8") as fout:
		fout.write(page)

main()
