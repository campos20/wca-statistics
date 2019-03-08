import json

def build_page(out):

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
	
	return page

def build_table(out):

	assert out["title"], "Title not found"
	assert out["table"], "Table not found"

	title = out["title"]
	table = "<h2>%s</h2>\n"%title
	
	if "subtitle" in out:
		table += "<p>%s</p>"%out["subtitle"]

	table += 			'  <table>\n'
	
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
