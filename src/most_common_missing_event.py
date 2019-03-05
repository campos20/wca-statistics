import csv, sys, math

from utils import get_wca_events

def missing_event(n):

	start_year = 2014 # current events
	wca_events = get_wca_events()

	assert 0<n<len(wca_events), "Number n of events must be 0<n<%s"%len(wca_events)

	with open('WCA_export/WCA_export_Competitions.tsv', newline='') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		
		event_list = []
		count = []

		header = True
		C = 0
		
		for line in tsvin:

			if header: # skip header.
				header = False
				continue

			# since events are added and removed, it makes sense to ignore competitions older than the current events set.
			year = int(line[5])
			if year < start_year:
				continue

			events = set(line[10].split())
			missing_events = wca_events - events

			if len(missing_events) == n:
				C += 1
				for x in missing_events:
					if x not in event_list:
						event_list.append(x)
						count.append(0)
					
					i = event_list.index(x)
					count[i] += 1

	number_for_fill = int(math.log10(max(count)))+1 # neat :)
	
	print("Number of times an event was ignored in a competition missing %s event%s since %s."%(n, "s"*(n>0), start_year))
	for x, y in sorted(zip(count, event_list))[::-1]:
		print(str(x).zfill(number_for_fill)+"\t"+y)

def main():
	"""Usage: python3 most_common_missing_event.py n
	n is the number of missing events in a competition.
	Let's say n == 1, then we will look for competition missing 1 event and we'll check the frequency of the missing event.
	"""

	args = sys.argv
	n = 0

	try:
		n = int(args[1])
	except:
		print("Please inform the number of missing events.")
		sys.exit(0)

	missing_event(n)

main()