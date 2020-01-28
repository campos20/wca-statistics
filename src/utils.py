import json
import pandas as pd
from math import *
import re

# WCA_export_Competitions labels
"""id name cityName countryId information [0-4]
year month day endMonth endDay [5-9]
eventSpecs wcaDelegate organiser [10-12]
venue venueAddress venueDetails [13-15]
external_website cellName latitude longitude [16-19]
"""

# WCA_export_Results labels
"""competitionId eventId roundTypeId pos [0-3]
best average personName personId personCountryId [4-8]
formatId value1 value2 value3 value4 value5 [9-14]
regionalSingleRecord regionalAverageRecord [15-16]
"""
# if ordered, then it's added
# year month day [17-19]


def get_set_wca_events():
    """Returns a set with all current WCA events as of
    https://www.worldcubeassociation.org/regulations/#9b"""

    return set("222 333 333bf 333fm 333ft 333mbf 333oh 444 444bf 555 555bf 666 777 clock minx pyram skewb sq1".split())


def get_export_date():
    with open('WCA_export/metadata.json', 'r') as f:
        array = json.load(f)

    return array["export_date"]


def html_link_format(text, link):
    return '<a href="%s">%s</a>' % (link, text)


def reduce_to_letters(s):
    out = ""
    for x in s:
        if x.isalpha():
            out += x
    return out


def avg(l):
    if len(l) == 0:
        return 0.
    return 1.0*sum(l)/len(l)


def parse_link(link):
    """Get link's text only"""
    if "<a href" in link:
        return link[link.index(">")+1: link.index("</a>")]
    return link


def get_competitor_link(wca_id):
    return "https://www.worldcubeassociation.org/persons/%s" % wca_id


def get_competition_html_link(competition_id):
    link = "https://www.worldcubeassociation.org/competitions/%s" % competition_id
    return html_link_format(competition_id, link)


def largest_range(lista):

    # LISTA MUST HAVE NO REPETITIONS AND IT MUST BE SORTED

    i = 0
    r = 1
    max_r = 0
    min_range = -1  # where the range started
    max_range = -1  # where the range ended
    STEP = 1  # if you want ranges in 2 (eg. 4, 6, 8), change here

    range_start = lista[i]
    range_end = lista[i]

    while i < len(lista)-1:

        if lista[i+1]-lista[i] == STEP:
            r += 1
        else:
            if r >= max_r:
                max_r = r
                max_range = lista[i]
                min_range = range_start

            range_start = lista[i+1]
            r = 1

        i += 1

    if r > max_r:
        max_r = r
        max_range = lista[i]
        min_range = range_start

    # len of range, start, end
    return (max_r, min_range, max_range)


def time_format(time):
    time = float(time)/100

    h = int(time/3600)
    time -= h*3600

    m = int(time/60)
    time -= m*60

    s = int(time)
    time -= s

    d = int(time*100)

    if h > 0:
        return "%s:%s:%s.%s" % (h, str(m).zfill(2), str(s).zfill(2), str(d).zfill(2))
    return "%s:%s.%s" % (str(m).zfill(2), str(s).zfill(2), str(d).zfill(2))


def get_competition_index_in_tsv(competition_id):
    # This does not consider the header, so, if it's not using pandas, better be sure if there's need to fix by 1.
    # Since competitions might have names capitalized or not, this messes with standard bisect.
    # So here is a new bisect, ignoring capitalization.

    data = (pd.read_csv(
        'WCA_export/WCA_export_Competitions.tsv', sep='\t'))["id"]

    id_upper = competition_id.upper()

    start = 0
    end = len(data)
    i = (start+end)/2

    while start < end:
        i = (start+end)/2
        if data[i].upper() < x:
            start = i+1
        else:
            end = i

    return i


def dist(lat1, lon1, lat2, lon2):
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

    R = 6373.0

    lat1 = radians(float(lat1)/pow(10, 6))
    lon1 = radians(float(lon1)/pow(10, 6))
    lat2 = radians(float(lat2)/pow(10, 6))
    lon2 = radians(float(lon2)/pow(10, 6))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R*c


def find_continent(countryId):
    data = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")
    continentId = data[data["id"] == countryId]["continentId"].to_string(
        index=False).strip()

    data = pd.read_csv("WCA_export/WCA_export_Continents.tsv", sep="\t")
    continent = data[data["id"] == continentId]["name"].to_string(
        index=False).strip()

    return continent


def find_name(countryId):
    """From XE to multiple countries europe, for example."""
    data = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep="\t")
    name = data[data["id"] == countryId]["name"].to_string(index=False).strip()
    return name


def iso2_country_name(countryId):
    country_list = pd.read_csv("WCA_export/WCA_export_Countries.tsv", sep='\t')
    countryId = countryId.strip()
    return country_list[country_list["iso2"] == countryId]["name"].values[-1]


def extract_delegate(line):
    """Delegates are written on a strange way on the export.
    This function extracts all of them.
    Example:
    [{Marlon de V. Marques}{mailto:mmarques@worldcubeassociation.org}] [{Murillo Gomes Otero}{mailto:motero@worldcubeassociation.org}] [{Pedro Santos Guimarães}{mailto:pguimaraes@worldcubeassociation.org}]"""
    out = []
    for x in re.findall("\[(.*?)\]", line):
        delegate = re.findall("\{(.*?)\}", x)
        delegate_name = delegate[0]
        out.append(delegate_name)
    return out


# print(dist(-16717151, -49254835, -15650789, -47806808))
