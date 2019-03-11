import csv, bisect, sys
from build_page import build_results
from utils import *

def wen_points():

	LIMIT = 100
	id_list = []
	name_list = []
	results = []
	display = []
	country_list = []
	
	with open('WCA_export/WCA_export_Results.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		for line in tsvin:

			event = line[1]
			
			if event != "333mbf":
				continue
			
			wca_id = line[7]
			
			i = bisect.bisect_left(id_list, wca_id)
			if i == len(id_list) or id_list[i] != wca_id:
				name = line[6]
				country = line[8]
				
				id_list.insert(i, wca_id)
				name_list.insert(i, name)
				country_list.insert(i, country)
				results.insert(i, -1)
				display.insert(i, None)
			
			for x in line[10:13]:
				if x in ["-2", "-1", "0"]: continue
				missed = int(x[-2:])
				DD = int(x[:2])
				difference = 99-DD
				solved = difference + missed
				attempted = solved + missed
				wen_points = 1.0*pow(solved,2)/attempted
				
				if wen_points > results[i]:
					results[i] = wen_points
					display[i] = "%s/%s"%(solved, attempted)
	
	prev = None
	count = 0
	pos = 0
	table = []
	for points, show, name, wca_id, country in sorted(zip(results, display, name_list, id_list, country_list))[::-1]:
		count += 1
		
		if count > LIMIT and prev != points:
			break
		
		pos = "-"
		if prev != points:
			pos = count
			if points < 0: break
		
		link = get_competitor_link(wca_id)
		table.append([pos, "%.2f"%points, show, html_link_format(name, link), country])

		prev = points
	
	out = {}
	out["table"] = table
	out["labels"] = ["#", "Wen points", "Result", "Name", "Country"]
	out["title"] = "Wen Points"
	out["explanation"] = "A Wen Point is a 333mbld result computed as (cubes solved^2)/(cubes attempted) or efficiency * attempted."
	
	return out

def main():
	args = sys.argv
	out = wen_points()
	
	build_results(out, args)

main()
