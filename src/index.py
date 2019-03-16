from os import listdir
from utils import html_link_format, get_export_date
import dateutil.parser
import json

# TODO find a better way to do this
# perhaps making every file a class and use class.get_link and class.get_title
# I'm not sure how to iterate over that yet

def main():

	script_opening = '<script id="data" type="application/json">'
	script_close = '</script>'
	
	template = open("template/index.html", "r", encoding="utf8").read()
	header = open("template/header.html", "r", encoding="utf8").read()
	top = open("template/top.html", "r", encoding="utf8").read()	
	left_bar = open("template/left_bar.html", "r", encoding="utf8").read()
	closing = open("template/closing.html", "r", encoding="utf8").read()
	
	date_stamp = dateutil.parser.parse(get_export_date()).date()

	table = []
	for f in listdir("pages/"):
		temp = f.split(".")
		if "stat-" in temp[0] and temp[-1] == "html":
			with open("pages/%s"%f, "r", encoding="utf8") as temp:
			
				# here we get the content inside each <script>'s page
				# this will work as long as nothing else goes on each script, except the json of each statistic
				data = temp.read()
				data = data[data.index(script_opening)+len(script_opening):]
				data = data[:data.index("</script>")]
				data = json.loads(data)
				
				title = data["title"]
				table.append([title, '      <li class="list-group-item list-group-item-action">%s</li>\n'%html_link_format(title, "%s"%f)])
	
	content =	'    <div class="col-sm-8">'
	content +=	'     <p>Export date: %s</p>'%date_stamp
	content +=	'     <ul class="list-group">\n'
	for x, y in sorted(table):
		content += y
	content +=	'     </ul>'
	content +=	'    </div>'
		
	page = template%(header, top, left_bar, content, closing)

	with open("pages/index.html", "w", encoding="utf8") as fout:
		fout.write(page)
	
main()
