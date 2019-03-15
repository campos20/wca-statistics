import sys, utils
import pandas as pd
from build_page import build_results

def missing_event(n):

	start_year = 2014 # current events
	wca_events = utils.get_set_wca_events()
	missing_event_count = {}

	assert 0<n<len(wca_events), "Number n of events must be 0<n<%s"%len(wca_events)

	data = pd.read_csv('WCA_export/WCA_export_Competitions.tsv', sep='\t')
	events = data[data["year"] >= start_year]["eventSpecs"]

	for x in events:
		events_set = set(x.split())
		diff = wca_events-events_set

		if len(diff) == n:
			for x in diff:
				if x not in missing_event_count:
					missing_event_count[x] = 0
				missing_event_count[x] += 1

	s = [(k, missing_event_count[k]) for k in sorted(missing_event_count, key=missing_event_count.get, reverse=True)]
	
	out = {}
	out["title"] = "Number of times an event was ignored in a competition missing %s event%s since %s"%(n, "s" if n>1 else "", start_year)
	out["labels"] = ["Event", "Number of times missing"]

	table = []
	for x, y in s:
		table.append([x, y])
	out["table"] = table
	
	return out

def main():
	"""Usage: python3 most_common_missing_event.py n
	n is the number of missing events in a competition.
	Let's say n == 1, then we will look for competitions missing 1 event and we'll check the frequency of the missing event.
	"""

	args = sys.argv
	n = 0

	try:
		n = int(args[1])
	except:
		n = 1 # we assume n=1
		
	stat = missing_event(n)
	args = sys.argv
	build_results(stat, args)

main()
