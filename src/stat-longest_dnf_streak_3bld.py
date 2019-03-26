import csv, bisect, sys
from build_page import build_results
from utils import *

def dnf_streak():

	LIMIT = 50
	id_list = []
	name_list = []
	country_list = []
	count_list = []
	max_list = []
	max_range_start = []
	max_range_end = []
	current_range_start = []
	
	with open('WCA_export/WCA_export_Results_Ordered.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		for line in tsvin:

			event = line[1]
			
			if event != "333bf":
				continue
			
			wca_id = line[7]
			
			i = bisect.bisect_left(id_list, wca_id)
			if i == len(id_list) or id_list[i] != wca_id:
				name = line[6]
				country = line[8]
				
				id_list.insert(i, wca_id)
				name_list.insert(i, name)
				country_list.insert(i, country)
				max_list.insert(i, 0)
				count_list.insert(i, 0)
				max_range_start.insert(i, None)
				max_range_end.insert(i, None)
				current_range_start.insert(i, None)
				
			for x in line[10:13]:

				x = int(x)
				if x > 0:
					count_list[i] = 0
				elif x == -1:
					count_list[i] += 1
					
					competition_id = line[0]

					if count_list[i] >= max_list[i]:
						max_list[i] = count_list[i]
						max_range_start[i] = current_range_start[i]
						max_range_end[i] = competition_id
					
					if count_list[i] == 1:
						current_range_start[i] = competition_id

	out = {}
	out["title"] = "DNF streak in 3BLD"
	out["labels"] = ["#", "DNF streak", "Name", "Country", "Start", "End"]
	out["explanation"] = 'Ongoing streaks are marked with "+".'
	
	table = []
	count = 1
	prev = None
	for streak, wca_id, name, current, country, start, end in sorted(zip(max_list, id_list, name_list, count_list, country_list, max_range_start, max_range_end))[::-1]:
		if count>LIMIT and prev != streak:
			break
		pos = "-"
		if streak != prev:
			pos = str(count)
		
		link = get_competitor_link(wca_id)
		table.append([pos, str(streak)+("+" if streak == current else ""), html_link_format(name, link), country, get_competition_html_link(start), "" if streak == current else get_competition_html_link(end)])
		
		count += 1
		prev = streak
	
	out["table"] = table
	
	return out

def main():
	args = sys.argv
	out = dnf_streak()
	
	build_results(out, args)

main()
