from utils import *
from build_page import build_results
from os import listdir
import json, sys

# TODO find a better way to do this
# perhaps making every file a class and use class.get_link and class.get_title
# I'm not sure how to iterate over that yet

def main():

	script_opening = '<script id="data" type="application/json">'
	script_close = '</script>'
	
	out = {}

	out["subtitle"] = "Export date: %s"%get_export_date()
	out["labels"] = ["Statistics"]
	
	table = []
	for f in listdir("pages/"):
		temp = f.split(".")
		if temp[0] != "main_page" and temp[-1] == "html":
			with open("pages/%s"%f, "r", encoding="utf8") as page:
			
				# here we get the content inside each <script>'s page
				# this will work as long as nothing else goes on each script, except the json of each statistic
				data = page.read()
				data = data[data.index(script_opening)+len(script_opening):]
				data = data[:data.index("</script>")]
				data = json.loads(data)
				
				title = data["title"]
				table.append([html_link_format(title, "%s"%f)])
	
	table = sorted(table)
	out["table"] = table
	
	args = sys.argv
	build_results(out, args)
	
main()
