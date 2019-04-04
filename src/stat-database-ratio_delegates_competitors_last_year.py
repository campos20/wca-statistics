import bisect, csv, datetime, sys
from build_page import build_results

# This stat uses some data from developer export (get the number of active delegates). So, make sure you run
# "generate-output-from-database.sh" before running this and that
# the developer export is downloaded and extracted.

def ratio_competitors_delegates():

	days = 365
	
	countries_delegates = []
	number_of_delegates = []

	file = open("database_out/stat-database-ratio_delegates_competitors_last_year.txt", "r").readlines()

	for line in file:
		temp = line.split()
		delegates = int(temp[-1])
		if delegates>0: # Avoid countries with 0 delegates. This prevents 0 division
			country = " ".join(temp[:-1])

			i = bisect.bisect_left(countries_delegates, country) # USA messes with ordering (capitalization), so here we sort this again (mysql isn't case sensitive for this matter)
			number_of_delegates.insert(i, delegates)
			countries_delegates.insert(i, country)

	competitors_last_year = []

	today = datetime.date.today()

	countries_persons = []
	competitors_id = []
	competitors_names = []

	tsvfile = open("WCA_export/WCA_export_Results_Ordered.tsv", "r")
	tsvreader = csv.reader(tsvfile, delimiter="\t")
	next(tsvreader, None)
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

	ratios = []
	competitors_out = []
	for i in range(len(countries_delegates)):
		country = countries_delegates[i]
		delegates = number_of_delegates[i]

		j = bisect.bisect_left(countries_persons, country)
		number_of_competitors = len(competitors_id[j])
		competitors_out.append(number_of_competitors)

		ratio = 1.0*number_of_competitors/delegates # 0 division is already avoided
		ratios.append(ratio)

	table = []
	c = 1
	prev = None
	for ratio, country, competitors, delegates in sorted(zip(ratios, countries_delegates, competitors_out, number_of_delegates))[::-1]:
		ratio_display = "%.2f"%ratio
		pos = c
		if ratio_display == prev:
			pos = "-"
		table.append([pos, ratio_display, country, competitors, delegates])
		c += 1
		prev = ratio_display

	no_delegates_country = []
	competitors_no_delegates = []
	for i in range(len(countries_persons)):
		country = countries_persons[i]
		j = bisect.bisect_left(countries_delegates, country)

		if j == len(countries_delegates) or countries_delegates[j] != country:
			no_delegates_country.append(country)
			competitors_no_delegates.append(len(competitors_id[i]))

	flag = True
	pos = c
	for competitor, country in sorted(zip(competitors_no_delegates, no_delegates_country))[::-1]:
		if not flag:
			pos = "-"
		table.append([pos, '<span style="color:red;">NA</span>', country, competitor, 0])
		flag = False

	out = {}
	out["title"] = "Ratio between number of active competitors in the last %s days and active delegates"%days
	out["labels"] = ["Pos", "Ratio", "Country", "Active competitors", "Delegates"]
	out["explanation"] = 'That is: active competitors/delegates. It\'s the virtual number each delegate had to handle in the past %s days (if everyone just competed is his home country). So, for the first position, %s, each one of the %s delegates had to deal with %s competitors on average in the past %s days. First considered date here is %s.'%(days, table[0][2], table[0][4], table[0][1], days, date-datetime.timedelta(days=days))
	out["table"] = table
	return out

def main():
	args = sys.argv
	out = ratio_competitors_delegates()
	build_results(out, args)

if __name__ == "__main__":
	main()