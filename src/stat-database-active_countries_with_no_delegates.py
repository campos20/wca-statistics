import bisect, csv, datetime, sys
from build_page import build_results

# This is basically the NA countries from stat-database-ratio_delegates_competitors_last_year.py

def no_delegates():

	days = 365
	
	countries_delegates = []

	# the file is there already, so we can use it
	file = open("database_out/stat-database-ratio_delegates_competitors_last_year.txt", "r").readlines()

	for line in file:
		temp = line.split()
		delegates = int(temp[-1])
		if delegates>0: # Avoid countries with 0 delegates. This prevents 0 division
			country = " ".join(temp[:-1])

			i = bisect.bisect_left(countries_delegates, country) # USA messes with ordering (capitalization), so here we sort this again (mysql isn't case sensitive for this matter)
			countries_delegates.insert(i, country)

	competitors_last_year = []

	today = datetime.date.today()

	countries_persons = []
	competitors_id = []
	competitors_names = []

	tsvfile = open("WCA_export/WCA_export_Results_Ordered.tsv", "r")
	tsvreader = csv.reader(tsvfile, delimiter="\t")
	next(tsvreader, None) # skip header
	for line in tsvreader: # bisect here?
		year, month, day = map(int, [line[17], line[18], line[19]])
		date = datetime.date(year, month, day)
		if date + datetime.timedelta(days=days) >= today:
			person_name = line[6]
			person_id = line[7]
			country = line[8]

			i = bisect.bisect_left(countries_persons, country)
			if i == len(countries_persons) or countries_persons[i] != country:
				countries_persons.insert(i, country)
				competitors_id.insert(i, [])
				competitors_names.insert(i, [])

			j = bisect.bisect_left(competitors_id[i], person_id)
			if j == len(competitors_id[i]) or competitors_id[i][j] != person_id:
				competitors_id[i].insert(j, person_id)
				competitors_names[i].insert(j, person_name)

	table = []
	no_delegates_country = []
	competitors_no_delegates = []
	for i in range(len(countries_persons)):
		country = countries_persons[i]
		j = bisect.bisect_left(countries_delegates, country)

		if j == len(countries_delegates) or countries_delegates[j] != country:
			no_delegates_country.append(country)
			competitors_no_delegates.append(len(competitors_id[i]))

	c = 1
	prev = None
	for competitors, country in sorted(zip(competitors_no_delegates, no_delegates_country))[::-1]:
		pos = c
		if competitors == prev:
			pos = "-"
		table.append([pos, competitors, country])
		c += 1
		prev = competitors

	out = {}
	out["title"] = "Active countries with no delegates in the last %s days"%days
	out["labels"] = ["Pos", "Active competitors", "Country"]
	out["explanation"] = '<a href="stat-database-ratio_delegates_competitors_last_year.html">Related</a>.'
	out["table"] = table
	return out

def main():
	args = sys.argv
	out = no_delegates()
	build_results(out, args)

if __name__ == "__main__":
	main()