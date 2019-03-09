import json

# WCA_export_Competitions labels
"""id name cityName countryId information [0-4]
year month day endMonth endDay [5-9]
eventSpecs wcaDelegate organiser [10-12]
venue venueAddress venueDetails [13-15]
external_website cellName latitude longitude [16-19]"""

# WCA_export_Results labels
"""competitionId eventId roundTypeId pos [0-3]
best average personName personId personCountryId [4-8]
formatId value1 value2 value3 value4 value5 [9-14]
regionalSingleRecord regionalAverageRecord [15-16]
"""

def get_set_wca_events():
	"""Returns a set with all current WCA events as of
	https://www.worldcubeassociation.org/regulations/#9b"""

	return set("222 333 333bf 333fm 333ft 333mbf 333oh 444 444bf 555 555bf 666 777 clock minx pyram skewb sq1".split())

def get_export_date():
	with open('WCA_export/metadata.json', 'r') as f:
		array = json.load(f)
		
	return array["export_date"]

def html_link_format(text, link):
	return '<a href="%s">%s</a>'%(link, text)

def reduce_to_letters(s):
	out = ""
	for x in s:
		if x.isalpha(): out += x
	return out

def avg(l):
	if len(l) == 0: return 0.
	return 1.0*sum(l)/len(l)

def parse_link(link):
	"""Get link's text only"""
	if "<a href" in link:
		return link[link.index(">")+1: link.index("</a>")]
	return link

def get_competitor_link(wca_id):
	return "https://www.worldcubeassociation.org/persons/%s"%wca_id

def largest_range(lista):

	# LISTA MUST HAVE NO REPETITIONS AND IT MUST BE SORTED

	i=0
	r=1
	max_r = 0
	min_range = -1 # where the range started
	max_range = -1 # where the range ended
	STEP = 1 # if you want ranges in 2 (eg. 4, 6, 8), change here
	
	range_start = lista[i]
	range_end = lista[i]
	
	while i<len(lista)-1:
		
		if lista[i+1]-lista[i] == STEP:
			r += 1
		else:
			if r >= max_r:
				max_r = r
				max_range = lista[i]
				min_range = range_start
			
			range_start = lista[i+1]
			r=1
			
		i += 1
	
	if r > max_r:
		max_r = r
		max_range = lista[i]
		min_range = range_start
	
	# len of range, start, end
	return (max_r, min_range, max_range)
