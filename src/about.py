def main():

    title = "WCA Statistics - About"

    template = open("template/basic.html", "r", encoding="utf8").read()
    header = open("template/header.html", "r", encoding="utf8").read()%title
    top = open("template/top.html", "r", encoding="utf8").read()
    nav_bar = open("template/nav_bar.html", "r", encoding="utf8").read()
    left_bar = open("template/left_bar.html", "r", encoding="utf8").read()
    text = open("template/about_text.txt", "r", encoding="utf8").read()
    closing = open("template/closing.html", "r", encoding="utf8").read()
    
    content = '    <div class="col-sm-8">\n'
    content += text
    content += '    </div>\n'
    
    page = template%(header, top, nav_bar, left_bar, content, closing)

    with open("pages/about.html", "w", encoding="utf8") as fout:
        fout.write(page)
    
main()
