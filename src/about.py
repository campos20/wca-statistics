from utils import html_link_format

def main():

	template = open("template/about.html", "r", encoding="utf8").read()
	header = open("template/header.html", "r", encoding="utf8").read()
	top = open("template/top.html", "r", encoding="utf8").read()	
	left_bar = open("template/left_bar.html", "r", encoding="utf8").read()
	text = open("template/about_text.txt", "r", encoding="utf8").read()
	closing = open("template/closing.html", "r", encoding="utf8").read()
	
	content = '    <div class="col-sm-8">'
	content += text
	content += '    </div>'
	
	page = template%(header, top, left_bar, content, closing)

	with open("pages/about.html", "w", encoding="utf8") as fout:
		fout.write(page)
	
main()
