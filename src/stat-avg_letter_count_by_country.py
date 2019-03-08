import csv
from utils import *
from build_page import build_page

def avg_letter():
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
				
			# remove spaces . and -
			name = reduce_to_letters(name)

			name_count = sum(map(len, name.split()))
			country = line[3]
			
			i = -1
			try:
				i = country_list.index(country)
			except:
				country_list.append(country)
				count.append([])
			count[i].append(name_count)
	
	limit = 100

	out = {}
	out["title"] = "Avg letter count by country"
	out["labels"] = ["#", "Avg", "Country", "# of competitors"]
	
	avg_list = map(avg, count)
	no_of_competitors = map(len, count)
	table = []
	count = 1
	prev = None
	for (x, y, z) in sorted(zip(avg_list, country_list, no_of_competitors))[::-1]:
		pos = "-"
		if x != prev:
			pos = count
		table.append([pos, "%.2f"%x, y, z])
		if len(table) >= limit:
			break
		count += 1
		prev = x

	out["table"] = table
		
	return out
	
def main():

	page = build_page(avg_letter())
	
	with open("pages/avg_letter_count_by_country.html", "w", encoding="utf8") as fout:
		fout.write(page)
			
main()
