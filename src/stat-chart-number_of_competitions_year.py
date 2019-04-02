import json, sys
import pandas as pd
from bisect import bisect_left

# for google chart
pre_header = """
    <!--Load the AJAX API-->
    <script src="https://www.gstatic.com/charts/loader.js"></script>
"""

content = """
    <div style="text-align: center">    
%s
     <div id="chart_div"></div>
    </div>
    <script src="tempCompetitionData.js"></script>
    <script src="chart.js"></script>
"""

page = open("template/stat.html", "r", encoding="utf8").read()

def new_competitors():

    data = pd.read_csv("WCA_export/WCA_export_Competitions.tsv", sep = "\t")
    
    countries = []
    years = []
    count = []
    
    for year, country in zip(data["year"], data["countryId"]):

        i = bisect_left(countries, country)
        if i == len(countries) or countries[i] != country:
            countries.insert(i, country)
            years.insert(i, [])
            count.insert(i, [])

        j = bisect_left(years[i], year)
        if j == len(years[i]) or years[i][j] != year:
            years[i].insert(j, year)
            count[i].insert(j, 0)
        
        count[i][j] += 1
    
    d = {}
    for i in range(len(countries)):
        temp = {}
        for j in range(len(years[i])):
            temp[years[i][j]] = count[i][j]
        d[countries[i]] = temp


    # https://github.com/thewca/worldcubeassociation.org/blob/16cdcd4d443dfae8be81ae1cdfd5f224a444f6f4/WcaOnRails/app/models/country.rb#L26
    multiple = {}
    multiple['XF'] = 'Multiple Countries (Africa)'
    multiple['XM'] = 'Multiple Countries (Americas)'
    multiple['XA'] = 'Multiple Countries (Asia)'
    multiple['XE'] = 'Multiple Countries (Europe)'
    multiple['XN'] = 'Multiple Countries (North America)'
    multiple['XO'] = 'Multiple Countries (Oceania)'
    multiple['XS'] = 'Multiple Countries (South America)'
    multiple['XW'] = 'Multiple Countries (World)'

    for x in d:
        if len(x) == 2 and x in multiple:
            d[multiple[x]] = d.pop(x)
    
    out = json.dumps(d, indent=2, sort_keys=True)
    
    selector_element = '      <option>%s</option>\n'
    selector = '     <select id="selector">\n'
    for country in d:
        selector += selector_element%country
    selector += '     </select>\n'
    
    title = "Number of competitions in each year by country"
    
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
    data = 'var label = "Competitions";\n'
    data += "var title = 'Number of competitions by year';\n"
    data += "var tableData = %s;\n"%out
    with open("pages/tempCompetitionData.js", "w", encoding="utf8") as fout:
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
