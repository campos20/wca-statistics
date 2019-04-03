import json, sys
import pandas as pd
from bisect import bisect_left
from utils import *

# There's a better explanation on how this works commented in the file stat-chart-number_of_competitions_year.py

# for google chart
pre_header = """
    <!--Load the AJAX API-->
    <script src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="tempCompetitorData.js"></script>
"""

content = """
    <div style="text-align: center">    
%s
     <div id="chart_div"></div>
    </div>
    <script src="chart.js"></script>
"""

page = open("template/stat.html", "r", encoding="utf8").read()

def new_competitors():

    data = pd.read_csv("WCA_export/WCA_export_Persons.tsv", sep = "\t")
    
    countries = []
    years = []
    count = []
    
    for subid, country in zip(data["id"], data["countryId"]):

        i = bisect_left(countries, country)
        if i == len(countries) or countries[i] != country:
            countries.insert(i, country)
            years.insert(i, [])
            count.insert(i, [])
        
        year = int(subid[:4])
        j = bisect_left(years[i], year)
        if j == len(years[i]) or years[i][j] != year:
            years[i].insert(j, year)
            count[i].insert(j, 0)
        
        count[i][j] += 1

    # fill in gaps
    for i in range(len(countries)):
        j = 1
        while j<len(years[i]):
            while years[i][j-1] != years[i][j]-1 and years[i][j-1] != 1982:
                years[i].insert(j, years[i][j]-1) 
                count[i].insert(j, 0)
            j += 1
    
    d = {}
    for i in range(len(countries)):
        temp = {}
        for j in range(len(years[i])):
            temp[years[i][j]] = count[i][j]
        d[countries[i]] = temp

    # Continents are handled separetely
    continent_dict = {}
    for x in d:
        continent = find_continent(x)
        if continent not in continent_dict:
            continent_dict[continent] = {}
        for year in d[x]:
            if year not in continent_dict[continent]:
                continent_dict[continent][year] = 0
            continent_dict[continent][year] += d[x][year]

    # World, sum of competitions in continents
    world = {}
    world["World"] = {} # handle the same way the other dicts
    for x in continent_dict:
        for year in continent_dict[x]:
            if year not in world["World"]:
                world["World"][year] = 0
            world["World"][year] += continent_dict[x][year]
    
    # This dict will be converted to js object
    out = {}
    for x in d:
        out[x] = d[x]
    out.update(continent_dict) # Therefore, we can append continents
    out.update(world) # And world
    out = json.dumps(out, indent=2, sort_keys=True)
    
    # Create html selector
    selector_element = '       <option>%s</option>\n'
    selector = '     <select id="selector">\n'

    # Add world region
    selector += '      <optgroup>'
    selector += selector_element%"World"
    selector += '      </optgroup>'

    # Add continents to selector
    selector += '      <optgroup>'
    continent_list = sorted([x for x in continent_dict])
    for continent in continent_list:
        selector += selector_element%continent
    selector += '      </optgroup>'

    # Add countries
    selector += '      <optgroup>'
    for country in d:
        selector += selector_element%country
    selector += '      </optgroup>'
    
    selector += '     </select>\n'
    
    title = "Number of new competitors in each year by region"
    
    args = sys.argv
    
    file_name = ""
    for x in args:
        x = x.split(".")
        if x[-1] == "py":
            x = x[0].split("/")
            file_name = x[-1]
            break
    
    assert len(file_name) > 0
    
    header = open("template/header.html", "r", encoding="utf8").read()%title
    nav_bar = open("template/nav_bar.html", "r", encoding="utf8").read()
    footer = (open("template/footer.html", "r", encoding="utf8").read())%("%s"%file_name)
    closing = open("template/closing.html", "r", encoding="utf8").read()
    
    # here we create a js just to be used
    data = 'var label = "New competitors";\n'
    data += "var title = 'Number of new competitors by year';"
    data += "var tableData = %s;\n"%out
    with open("pages/tempCompetitorData.js", "w", encoding="utf8") as fout:
        fout.write(data)
    
    # create a copy of the .js inside the pages folder
    chart = open("src/chart.js", "r", encoding="utf8").read()
    with open("pages/chart.js", "w", encoding="utf8") as fout:
        fout.write(chart)
    
    title = '<h1 style="text-align:center">%s</h1>\n'%title
    explanation = ""
    
    with open("pages/%s.html"%file_name, "w", encoding="utf8") as fout:
        fout.write(page%(pre_header+header, nav_bar, title, explanation, content%selector, footer, closing))
    
def main():
    new_competitors()
    
main()
