from utils import html_link_format

def main():

	template = open("template/about_template.html", "r", encoding="utf8")
	text = open("template/about_text.txt", "r", encoding="utf8")
		
	page = template.read()%text.read()

	with open("pages/about.html", "w", encoding="utf8") as fout:
		fout.write(page)
	
main()
