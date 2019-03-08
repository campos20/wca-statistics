# avg number of comps per country since 2010
# we are taking the average of the number of comps/year since 2010.

import csv, sys
from utils import *
from build_page import build_results

def avg_competitions():
	country_list = []
	comp_year = []
	avg_list = []

	base_year = 2010
	max_year = base_year
	header = True
	discard = 1 # ignore countries with 1 competition

	with open('WCA_export/WCA_export_Competitions.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
				
		for line in tsvin:

			if header == 1:
				header = False
				continue
			
			year = int(line[5])
			if year < base_year: continue
			
			max_year = max(max_year, year)

			country = line[3]			
			if country not in country_list:
				country_list.append(country)
				comp_year.append([])
			
			i = country_list.index(country)
			
			while len(comp_year[i]) < year-base_year+1:
				comp_year[i].append(0)
			
			comp_year[i][year-base_year] += 1 # 2010 is 0, 2011 is 1, etc. we add 1 for each comp
			
		for x in comp_year:
			avg_list.append(avg(x))
		
		out = {}
		out["title"] = "Avg number of competitions per year by country since %s"%base_year
		out["labels"] = ["#", "Avg", "Country"]
		
		for year in range(base_year, max_year+1):
			out["labels"].append(year)
		
		table = []
		prev = None # tied stats
		count = 1
		for (x, y, z) in sorted(zip(avg_list, country_list, comp_year))[::-1]:
			if sum(z) <= discard: continue
			pos = "-"
			if prev != "%.2f"%x:
				pos = count
			table.append([pos, ("%.2f"%x).zfill(5), y])
			for competition_number in z:
				table[-1].append(competition_number)
			count += 1
			prev = "%.2f"%x
		out["table"] = table
	return out

def main():
	args = sys.argv
	
	stat = avg_competitions()
	build_results(stat, args)
	
main()
