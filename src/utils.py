
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
