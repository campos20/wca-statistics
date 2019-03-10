import csv, bisect, sys
from build_page import build_results
from utils import *

def sub30_fmc():

	LIMIT = 50
	id_list = []
	name_list = []
	country_list = []
	count_list = []
	max_list = []
	
	hold = 30
	
	with open('WCA_export/WCA_export_Results_Ordered.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		for line in tsvin:

			event = line[1]
			
			if event != "333fm":
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
				
			for x in line[10:13]:

				x=int(x)
				if x == -1 or x >= hold:
					count_list[i] = 0
				elif 0 < x < hold:
					count_list[i] += 1
					max_list[i] = max(max_list[i], count_list[i])

	out = {}
	out["title"] = "Most consecutive sub%s FMC"%hold
	out["labels"] = ["#", "Sub %s streak"%hold, "Name", "Country"]
	out["explanation"] = 'Ongoing streaks are marked with "+".'
	
	table = []
	count = 1
	prev = None
	for streak, wca_id, name, current, country in sorted(zip(max_list, id_list, name_list, count_list, country_list))[::-1]:
		if count>LIMIT and prev != streak:
			break
		pos = "-"
		if streak != prev:
			pos = str(count)
		
		link = get_competitor_link(wca_id)
		table.append([pos, str(streak)+("+" if streak == current else ""), html_link_format(name, link), country])
		
		count += 1
		prev = streak
	
	out["table"] = table
	
	return out

def main():
	args = sys.argv
	out = sub30_fmc()
	
	build_results(out, args)

main()
