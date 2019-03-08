import csv, sys
from build_page import build_results

def common_id():

	limit = 100
	
	table = []
	with open('WCA_export/WCA_export_Persons.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		id_list = []
		count = []
		
		for line in tsvin:
			wca_id = line[0][4:8]
			
			if wca_id not in id_list:
				id_list.append(wca_id)
				count.append(0)
			
			i = id_list.index(wca_id)
			count[i] += 1
		
		c = 1
		previous = 0
		
		for x, y in sorted(zip(count, id_list))[::-1]:
		
			pos = "-"
			if x != previous:
				pos = c
			if c>limit and previous != x: break
			table.append([pos, x, y])
			previous = x
			c += 1
	
	out = {}
	out["title"] = "Top %s most common 4 letters in WCA"%limit
	out["labels"] = ["Pos", "Count", "Letters"]
	out["table"] = table
	
	return out

def main():
	stat = common_id()
	args = sys.argv
	build_results(stat, args)
	
main()
