import sys, bisect, csv
from build_page import build_results
import pandas as pd
from utils import *

def get_far_comp():

	tsvin = open('WCA_export/WCA_export_Competitions.tsv')
	tsvin = csv.reader(tsvin, delimiter='\t')
	
	comps_id = []
	latitudes = []
	longitudes = []
	
	header = True
	for line in tsvin:
		if header:
			header = False
			continue
		comps_id.append(line[0].upper())
		latitudes.append(line[18])
		longitudes.append(line[19])
	del tsvin

	data = pd.read_csv("WCA_export/WCA_export_Results_Ordered.tsv", sep = "\t")
	
	wca_ids = []
	names = []
	competitions = []
	competitor_lat = []
	competitor_lon = []
	
	for competition, wca_id, name in zip(data["competitionId"], data["personId"], data["personName"]):

		i = bisect.bisect_left(wca_ids, wca_id)
		if i == len(wca_ids) or wca_ids[i] != wca_id:
			wca_ids.insert(i, wca_id)
			names.insert(i, name)
			competitions.insert(i, [])
			competitor_lat.insert(i, [])
			competitor_lon.insert(i, [])
		
		if len(competitions[i]) == 0 or competition != competitions[i][-1]:
			competitions[i].append(competition)
			
			j = bisect.bisect_left(comps_id, competition.upper())
			competitor_lat[i].append(latitudes[j])
			competitor_lon[i].append(longitudes[j])
	
	max_dists = []
	max_comp1 = []
	max_comp2 = []
	for i in range(len(wca_ids)):
		max_dists.append(0)
		max_comp1.append(None)
		max_comp2.append(None)
		if len(competitions[i]) > 1:
			for j in range(1, len(competitions[i])):
				D = dist(competitor_lat[i][j-1], competitor_lon[i][j-1], competitor_lat[i][j], competitor_lon[i][j])
				
				if D > max_dists[i]:
					max_dists[i] = D
					max_comp1[i] = competitions[i][j-1]
					max_comp2[i] = competitions[i][j]
			
	table = []
	
	limit = 100
	count = 1
	prev = None
	for D, name, wca_id, comp1, comp2 in sorted(zip(max_dists, names, wca_ids, max_comp1, max_comp2))[::-1]:
		D = "%.2f"%D
		pos = "-"
		if prev != D:
			pos = count
		if count > limit and prev != D:
			break
		link = get_competitor_link(wca_id)
		table.append([pos, D, html_link_format(name, link), get_competition_html_link(comp1), get_competition_html_link(comp2)])
		count += 1
		prev = D
	
	out = {}
	out["title"] = "Top far consecutive competition distance"
	out["labels"] = ["#", "Distance (km)", "Name", "Competition1", "Competition2"]
	out["table"] = table
	
	return out
	
def main():
	
	out = get_far_comp()
	args = sys.argv
	
	build_results(out, args)

main()
