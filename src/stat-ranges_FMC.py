import csv, sys, bisect
from utils import *
from build_page import build_results

def largest_range_fmc():

	LIMIT = 50
	lists_of_results = []
	id_list = []
	name_list = []
	country_list = []
	
	with open('WCA_export/WCA_export_Results.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		skip_header = True
		for line in tsvin:
		
			event = line[1]
			if skip_header or event != "333fm":
				skip_header = False
				continue
			
			name = line[6]
			wca_id = line[7]
			country = line[8]
			i = bisect.bisect_left(id_list, wca_id)
			if i == len(id_list) or id_list[i] != wca_id:
				name_list.insert(i, name)
				id_list.insert(i, wca_id)
				lists_of_results.insert(i, [])
				country_list.insert(i, country)
			
			for x in line[10:13]:
				x=int(x)
				if x>0:
					j = bisect.bisect_left(lists_of_results[i], x)
					if j == len(lists_of_results[i]) or lists_of_results[i][j] != x:
						lists_of_results[i].insert(j, x)

	name_out = []
	range_out = []
	min_out = []
	max_out = []
	id_list_out = []
	country_list_out = []
	
	for i in range(len(id_list)):
		if len(lists_of_results[i])<1: # skipping people with only 1 result
			continue
		name_out.append(name_list[i])
		id_list_out.append(id_list[i])
		country_list_out.append(country_list[i])
		a, b, c = largest_range(lists_of_results[i])
		range_out.append(a)
		min_out.append(b)
		max_out.append(c)
		

	table = []
	
	prev = None
	count = 0
	pos = 0
	for a, b, c, name, country, wca_id in sorted(zip(range_out, min_out, max_out, name_out, country_list_out, id_list_out))[::-1]:
		count += 1
		
		if count >= LIMIT and prev != a:
			break
		pos = "-"
		if prev != a:
			pos = count
		link = get_competitor_link(wca_id)
		table.append([pos, a, html_link_format(name, link), country, b, c])
		
		prev = a
	out = {}
	out["title"] = "Range in FMC"
	out["explanation"] = "Range here means no gap."
	out["labels"] = ["#", "Range", "Person", "Country", "Range Start", "Range End"]
	out["table"] = table
	return out

def main():
	args = sys.argv
	out = largest_range_fmc()
	
	build_results(out, args)

main()
