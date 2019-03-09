from utils import *
from build_page import build_results
from os import listdir
from datetime import datetime
import dateutil.parser
import json, sys

# TODO find a better way to do this
# perhaps making every file a class and use class.get_link and class.get_title
# I'm not sure how to iterate over that yet

def main():

	script_opening = '<script id="data" type="application/json">'
	script_close = '</script>'
	
	page =			"<html>\n"
	
	# head
	page +=			" <head>\n"
	page +=			' <link rel="stylesheet" type="text/css" href="index.css">\n'
	page +=			" </head>\n"

	# body
	page +=			" <body>\n"
	page +=			'<h2>Statistics</h2>\n'
	date_stamp =	'<p class="subtitle">Export date: %s</p>\n'%(dateutil.parser.parse(get_export_date()).date())
	page +=			date_stamp
	
	page += 		'  <table>\n'
	for f in listdir("pages/"):
		temp = f.split(".")
		if temp[0] != "index" and temp[-1] == "html":
			with open("pages/%s"%f, "r", encoding="utf8") as temp:
			
				# here we get the content inside each <script>'s page
				# this will work as long as nothing else goes on each script, except the json of each statistic
				data = temp.read()
				data = data[data.index(script_opening)+len(script_opening):]
				data = data[:data.index("</script>")]
				data = json.loads(data)
				
				title = data["title"]
				page += "   <tr><th>%s</th></tr>\n"%html_link_format(title, "%s"%f)
	
	page +=			" </body>\n"

	page +=		"</html>\n"
	
	with open("pages/index.html", "w", encoding="utf8") as fout:
		fout.write(page)
	
main()
