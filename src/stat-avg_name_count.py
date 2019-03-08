import csv, sys
from utils import *
from build_page import build_results

def avg_name_count():
	country_list = []
	count = []
	
	header = True

	with open("WCA_export/WCA_export_Persons.tsv") as tsvfile:

		tsvreader = csv.reader(tsvfile, delimiter="\t")
		for line in tsvreader:
		
			if header:
				header = False
				continue
		
			name = line[2]
			if "(" in name:
				name = name[:name.index("(")]
			
			name_count = len(name.split())
			country = line[3]
			
			i = -1
			try:
				i = country_list.index(country)
			except:
				country_list.append(country)
				count.append([])
			count[i].append(name_count)

	out = {}
	
	avg_list = map(avg, count)
	no_of_competitors = map(len, count)
	
	out["title"] = "Avg name count by country"
	out["labels"] = ["#", "Avg", "Country", "# of competitors"]
	
	table = []
	prev = None
	count = 1
	for x, y, z in sorted(zip(avg_list, country_list, no_of_competitors))[::-1]:
		pos = "-"
		if prev != "%.2f"%x:
			pos = count
		table.append([pos, "%.2f"%x, y, z])
		count += 1
		prev = "%.2f"%x
	out["table"] = table
	
	return out

def main():

	stat = avg_name_count()
	args = sys.argv
	build_results(stat, args)
	
main()
