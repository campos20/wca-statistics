from utils import parse_link
import os

def build_results(out, args):
    """Either build a page or show results on terminal."""
    
    allowed = ["title", "table", "labels", "explanation"]
    for x in out:
        assert x in allowed, "Unrecognized key %s"%x
    assert "title" in out, "Title not found"

    build = False
    for x in args:
        if "=" in x:
            var, value = x.split("=")
            if var == "page" and value == "true":
                build = True
                break
    
    if build:

        file_name = ""
        for x in args:
            x = x.split(".")
            if x[-1] == "py":
                x = x[0].split("/")
                file_name = x[-1]
                break
        
        assert len(file_name) > 0
        
        header = open("template/header.html", "r", encoding="utf8").read()%out["title"]
        nav_bar = open("template/nav_bar.html", "r", encoding="utf8").read()
        
        formated_title = '<h2 class="text-center">%s</h2>\n'%out["title"]
        explanation = ""
        if "explanation" in out:
            explanation = "<p>%s</p>"%out["explanation"]
            
        content = build_table(out)
        footer = open("template/footer.html", "r", encoding="utf8").read()%file_name
        closing = open("template/closing.html", "r", encoding="utf8").read()

        page = open("template/stat.html", "r", encoding="utf8").read()%(header, nav_bar, formated_title, explanation, content, footer, closing)
        
        if not os.path.exists("pages"):
            os.makedirs("pages")
        with open("pages/%s.html"%file_name, "w", encoding="utf8") as fout:
            fout.write(page)
    
    else:
        labels = out["labels"]
        print("\t".join(map(str, labels)))

        for x in out["table"]:
            print("\t".join(map(parse_link, (map(str, x)))))

def build_table(out):

    assert out["table"], "Table not found."
    
    table = ""

    table +=                 '  <table class="table table-striped table-bordered table-hover">\n'
    
    if "labels" in out:
        table +=            '   <thead class="thead-dark">'
        table +=            "     <tr>\n"
        for x in out["labels"]:
            table +=        '      <th class="text-center" scope="col">%s</th>\n'%x
        table +=            "     </tr>\n"
        table +=            '   </thead>'

    table +=                '   <tbody>'
    for x in out["table"]:

        assert type(x) is list, "A list was expected."
        
        table +=            "    <tr>\n"
        for y in x:
            table +=        '     <td class="text-center">%s</td>\n'%y
        table +=            "    </tr>\n"
    table +=                '   <tbody>'
    table +=                "  </table>\n"
    
    return table
