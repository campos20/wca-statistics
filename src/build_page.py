import json
from utils import parse_link

def build_results(out, args):
    """Either build a page or show results on terminal."""
    
    allowed = ["title", "table", "labels", "subtitle", "explanation"]
    for x in out:
        assert x in allowed, "Unrecognized key %s"%x

    build = False
    for x in args:
        if "=" in x:
            var, value = x.split("=")
            if var == "page" and value == "true":
                build = True
                break
    
    if build:

        page =             "<!DOCTYPE HTML>\n"
        page +=         '<html lang="en">\n'
        
        page +=            " <head>\n"
        page +=            '  <title>%s</title>\n'%out["title"]
        page +=         '  <meta charset="utf-8">'
        
        # bootstrap
        page +=         '  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'
        page +=         '  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'
        
        page +=            " </head>\n"
        
        page +=            " <body>\n"
        body = build_table(out)
        page += body
        
        page += "<p>Send suggestions or report bugs to acampos@worldcubeassociation.org</p>\n"
        page += '<p>This site is open source. Check the code <a href="https://github.com/campos20/wca-statistics/blob/master/%s">here</a>.</p>\n'%args[0]
        
        page +=            " </body>\n"
        
        page +=            "</html>"
        
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

    title = out["title"]
    table += '<h2 class="text-center">%s</h2>\n'%title
    
    if "subtitle" in out:
        table += "<h3>%s</h3>\n"%out["subtitle"]

    if "explanation" in out:
        table += '<p>%s</p>\n'%out["explanation"]

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
