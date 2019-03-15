import sys
from utils import *
from build_page import build_results
import pandas as pd

def count_letter(name):
	if "(" in name:
		name = name[:name.index("(")]
	name = reduce_to_letters(name)
	return sum(map(len, name.split()))

def biggest_names():

	data = pd.read_csv("WCA_export/WCA_export_Persons.tsv", sep = "\t")
	data["letters"] = [count_letter(x) for x in data["name"]]
	
	data.sort_values(by=["letters"], ascending=False, inplace=True)
	data.index = range(len(data["name"]))

	out = {}
	out["title"] = "Biggest names letter count"
	out["labels"] = ["#", "Count", "Name", "Country"]
	
	limit = 150
	table = []
	count = 1
	prev = None
	for i in range(len(data["name"])):
		pos = "-"
		letters = (data["letters"])[i]
		if count > limit and prev != letters:
			break
		if letters != prev:
			pos = count
		table.append([pos, str(letters), html_link_format((data["name"])[i], (data["id"])[i]), (data["countryId"])[i]])
		count += 1
		prev = letters

	out["table"] = table
		
	return out
	
def main():

	args = sys.argv
	stat = biggest_names()
	build_results(stat, args)
			
main()
