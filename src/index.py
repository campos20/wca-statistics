from os import listdir
from utils import html_link_format, get_export_date
import dateutil.parser
import json

# TODO find a better way to do this
# perhaps making every file a class and use class.get_link and class.get_title
# I'm not sure how to iterate over that yet

def main():

    title_opening = '<title>'
    title_close = '</title>'
    
    title = "WCA Statistics"
    
    template = open("template/basic.html", "r", encoding="utf8").read()
    header = open("template/header.html", "r", encoding="utf8").read()%title
    top = open("template/top.html", "r", encoding="utf8").read()
    nav_bar = open("template/nav_bar.html", "r", encoding="utf8").read()
    left_bar = open("template/left_bar.html", "r", encoding="utf8").read()
    closing = open("template/closing.html", "r", encoding="utf8").read()
    
    date_stamp = dateutil.parser.parse(get_export_date()).date()

    table = []
    for f in listdir("pages/"):
        temp = f.split(".")  

        if "stat-" in temp[0] and temp[-1] == "html":
            with open("pages/%s"%f, "r", encoding="utf8") as stat:          
            
                # here we get the title inside each statistics
                title = stat.read()
                title = title[title.index(title_opening)+len(title_opening):]
                title = title[:title.index(title_close)]
                
                chart = False
                if "-chart-" in temp[0]:
                    chart = True    
                
                if chart:
                    title = title + " [Chart]"
                
                table.append([title, '      <li class="list-group-item list-group-item-action">%s</li>\n'%html_link_format(title, "%s"%f)])
    
    content =    '    <div class="col-sm-8">\n'
    content +=    '     <p>Export date: %s</p>\n'%date_stamp
    content +=    '     <ul class="list-group">\n'
    for x, y in sorted(table):
        content += y
    content +=    '     </ul>'
    content +=    '    </div>'
        
    page = template%(header, top, nav_bar, left_bar, content, closing)

    with open("pages/index.html", "w", encoding="utf8") as fout:
        fout.write(page)
    
main()
