import csv, bisect, sys
from utils import *
from build_page import build_results

def most_dnf_ratio():

	with open("WCA_export/WCA_export_Results.tsv") as tsvfile:

		tsvreader = csv.reader(tsvfile, delimiter="\t")
		
		ids = []
		names = []
		countries = []
		results_count = []
		attempts_count = []
		dnf_count = []

		exclude = ["333bf", "444bf", "555bf", "333fm", "333mbf", "333mbo"]
		
		header = True

		for line in tsvreader:
		
			event = line[1]
			if event in exclude or header:
				header = False
				continue
			
			this_id = line[7]
			
			i = bisect.bisect_left(ids, this_id)
			if i == len(ids) or ids[i] != this_id:
				name = line[6]
				country = line[8]

				ids.insert(i, this_id)
				names.insert(i, name)
				countries.insert(i, country)
				
				results_count.insert(i, 0)
				dnf_count.insert(i, 0)
				attempts_count.insert(i, 0)
			
			for x in line[10:15]:
				x=int(x)
				if x == -1:
					dnf_count[i] += 1
					attempts_count[i] += 1
				elif x > 0:
					results_count[i] += 1
					attempts_count[i] += 1
					
		ratios = []
		out_names = []
		out_countries = []
		out_results = []
		out_dnf = []
		out_attempt = []
		out_ids = []
		
		hold = 200 # competitor must have at least 200 results
		limit = 100
		
		for i in range(len(ids)):
			attempts = attempts_count[i]
			result = results_count[i]
			if attempts < hold or result == 0:
				continue
			
			name = names[i]
			country = countries[i]
			dnf = dnf_count[i]
			
			out_names.append(name)
			out_countries.append(country)
			out_results.append(result)
			out_dnf.append(dnf)
			out_attempt.append(attempts)
			ratios.append(1.0*dnf/attempts)
			out_ids.append(ids[i])
		
		out = {}
		out["labels"] = ["#", "DNF Ratio (%)", "Name", "Country", "DNF", "Attempts"]
		table = []
		
		prev = None
		count = 0		
		for ratio, name, country, dnf, attempt, wca_id in sorted(zip(ratios, out_names, out_countries, out_dnf, out_attempt, out_ids)):
			count += 1
			
			ratio_out = "%.2f"%(100*ratio)
			if count > limit and prev != ratio_out:
				break
			
			pos = "-"
			if prev != ratio_out:
				pos = count
			
			table.append([pos, ratio_out, html_link_format(name, get_competitor_link(wca_id)), country, dnf, attempt])
			
			prev = ratio_out
		
		out["table"] = table
		out["title"] = "Lowest DNF ratio excluding BLD and FMC events"
		out["explanation"] = "Listing people with at least %s solutions."%hold
	
		return out
		
def main():
	args = sys.argv
	out = most_dnf_ratio()
	
	build_results(out, args)
	
main()
