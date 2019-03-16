import csv, sys, bisect
from build_page import build_results

def common_id():

	limit = 100
	
	table = []
	with open('WCA_export/WCA_export_Persons.tsv') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		id_list = []
		count = []
		
		for line in tsvin:
			letters = line[0][4:8]
			
			i = bisect.bisect_left(id_list, letters)
			if i == len(id_list) or letters != id_list[i]:
				id_list.insert(i, letters)
				count.insert(i, 0)
			
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
	out["title"] = "Most common sub-id"
	out["labels"] = ["Pos", "Count", "Sub-id"]
	out["explanation"] = "The sub-id is the 4 letters from each WCA ID."
	out["table"] = table
	
	return out

def main():
	stat = common_id()
	args = sys.argv
	build_results(stat, args)
	
main()
