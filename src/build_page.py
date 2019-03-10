import json
from utils import parse_link

def build_results(out, args):
	"""Either build a page or show results on terminal."""

	build = False
	for x in args:
		if "=" in x:
			var, value = x.split("=")
			if var == "page" and value == "true":
				build = True
	
	if build:

		page = 			""
		page += 			"<html>\n"
		
		page +=			" <head>\n"
		page +=			'  <link rel="stylesheet" type="text/css" href="styles.css">\n'
		
		page +=			'  <script id="data" type="application/json">'
		page +=			str(json.dumps(out)) # embed json
		page +=			'  </script>\n'
		page +=			" </head>\n"
		
		page +=			" <body>\n"
		body = build_table(out)
		page += body
		page +=			" </body>\n"
		
		page +=			"</html>"
		
		file_name = args[0].split("/")
		if "stat-" in file_name:
			file_name = args[0].split("stat-")[1]
		else:
			file_name = file_name[-1]
		file_name = file_name.replace(".py", ".html")
		
		with open("pages/%s"%file_name, "w", encoding="utf8") as fout:
			fout.write(page)
	
	else:
		labels = out["labels"]
		print("\t".join(map(str, labels)))

		for x in out["table"]:
			print("\t".join(map(parse_link, (map(str, x)))))

def build_table(out):

	assert out["table"], "Table not found."
	assert out["title"], "Title not found."
	
	table = ""

	if "title" in out:
		title = out["title"]
		table += "<h2>%s</h2>\n"%title
	
	if "subtitle" in out:
		table += "<p>%s</p>\n"%out["subtitle"]

	table += 			'  <table>\n'
	
	if "explanation" in out:
		table += '<p class="explanation">%s</p>\n'%out["explanation"]
	
	if "labels" in out:
		table +=			"	<tr>\n"
		for x in out["labels"]:
			table +=		"	 <th>%s</th>\n"%x
		table +=			"	</tr>\n"
	
	for x in out["table"]:

		assert type(x) is list, "A list was expected."
		
		table += 		"   <tr>\n"
		for y in x:
			table +=	"	<td>%s</td>\n"%y
		table += 		"   </tr>\n"
	table += 			"  </table>\n"
	
	return table
