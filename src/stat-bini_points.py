import csv, sys, bisect
from utils import *
from build_page import build_results

def bini_points():

	LIMIT = 100

	competitors_list = []
	competitors_point = []
	name_list = []
	country_list = []
	
	with open('WCA_export/WCA_export_Results.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		skip_header = True
		for line in tsvin:
		
			event = line[1]
			if skip_header or event in ["333fm", "333mbf", "333mbo"]:
				skip_header = False
				continue
			
			wca_id = line[7]
			name = line[6]
			country = line[8]
			
			i = bisect.bisect_left(competitors_list, wca_id)
			if i == len(competitors_list) or competitors_list[i] != wca_id: # insort like
				competitors_list.insert(i, wca_id)
				competitors_point.insert(i,0)
				name_list.insert(i, name)
				country_list.insert(i, country)
			
			for x in line[10:15]:
			
				time = int(x)
				if time<=0 or time >= 60000: # time=0, -1 or -2 is either DNF, DNS or no result
					continue

				if time%100 == 0:
					competitors_point[i] += 1

	out = {}
	out["title"] = "Top %s Bini points"%LIMIT
	out["explanation"] = "A Bini point is a result that ends in 00, excluding FMC, MBLD and results over 10 min."
	out["labels"] = ["#", "Bini Points", "Name", "Country"]
	
	table = []
	prev = None
	count = 1
	for points, name, country, wca_id in sorted(zip(competitors_point, name_list, country_list, competitors_list))[::-1]:
		if count > LIMIT and prev != points:
			break
		pos = "-"
		if prev != points:
			pos = count
		link = "https://www.worldcubeassociation.org/persons/%s"%wca_id
		table.append([pos, points, html_link_format(name, link), country])
		prev = points
		count += 1
	out["table"] = table
	
	return out

def main():
	args = sys.argv
	out = bini_points()
	
	build_results(out, args)

main()
