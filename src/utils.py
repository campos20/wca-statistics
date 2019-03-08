import json

# WCA_export_Competitions label
"""id name cityName countryId information [0-4]
year month day endMonth endDay [5-9]
eventSpecs wcaDelegate organiser [10-12]
venue venueAddress venueDetails [13-15]
external_website cellName latitude longitude [16-19]"""

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
