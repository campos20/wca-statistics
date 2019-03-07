def build_page(out):

	page = 			""
	page += 			"<html>\n"
	
	page +=			" <head>\n"
	page +=			'  <link rel="stylesheet" type="text/css" href="styles.css">\n'
	page +=			" </head>\n"
	
	page +=			" <body>\n"
	body = build_table(out)
	page += body
	page +=			" </body>\n"
	
	page +=			"</html>"
	
	return page

def build_table(out):

	assert len(out) > 2, "The table must have, at least, [header, specs, content..]"

	title = out[0]
	table = "<h2>%s</h2>\n"%title

	table += 			'  <table>\n'
	
	table +=			"    <tr>\n"
	for x in out[1]:
		table +=		"     <th>%s</th>\n"%x
	table +=			"    </tr>\n"
	
	for x in out[2:]:
		table += 		"   <tr>\n"
		for y in x:
			table +=	"    <td>%s</td>\n"%y
		table += 		"   </tr>\n"
	table += 			"  </table>\n"
	
	return table
