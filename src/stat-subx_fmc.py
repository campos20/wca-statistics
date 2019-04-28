from bisect import bisect_left
import csv
import json
import sys


def main():

    LIMIT = 30  # We only consider sub LIMIT results

    competitors_id = []
    names = []
    countries = []
    results_count = []

    wr_single = None

    with open("WCA_export/WCA_export_Results.tsv") as tsvfile:

        tsvreader = csv.reader(tsvfile, delimiter="\t")

        header = True
        for line in tsvreader:

            if header:
                header = False
                continue

            event, competitor_id, name, country = line[1], line[7], line[6], line[8]
            if event == "333fm":

                i = bisect_left(competitors_id, competitor_id)
                if i == len(competitors_id) or competitors_id[i] != competitor_id:
                    competitors_id.insert(i, competitor_id)
                    names.insert(i, name)
                    results_count.insert(i, [0 for j in range(LIMIT)])
                    countries.insert(i, country)

                for result in map(int, line[10:13]):
                    if 0 < result < LIMIT:
                        results_count[i][result-1] += 1
                        if wr_single == None or result < wr_single:
                            wr_single = result

    out = {}
    for j in range(wr_single, LIMIT):
        j_sum = [sum(x[wr_single-1: j]) for x in results_count]
        temp = []
        for s, name, competitor_id, country in sorted(zip(j_sum, names, competitors_id, countries))[::-1][:100]:
            if s == 0:
                break
            temp.append({"moves": s, "name": name,
                         "competitor_id": competitor_id, "country": country})

        out[j+1] = temp

    create_page(out)


def create_page(out):

    file_name = "stat-subx_fmc"
    for x in sys.argv:  # Double check
        if ".py" in x:
            x = x.split("/")[-1].split(".")[0]
            file_name = x

    title = "Sub X FMC"

    # Export data as js file
    with open("pages/data-subx_fmc.js", "w", encoding="utf8") as fout:
        fout.write(('var title = "%s";\n' %
                    title)+("var data = %s;" % json.dumps(out, indent=2)))

    # Copy js file
    js_file = open("src/js-subx_fmc.js", "r", encoding="utf8").read()
    with open("pages/js-subx_fmc.js", "w", encoding="utf8") as fout:
        fout.write(js_file)
    query_file = open("src/useQueryParameter.js", "r", encoding="utf8").read()
    with open("pages/useQueryParameter.js", "w", encoding="utf8") as fout:
        fout.write(query_file)

    content = '<div id="content"></div>\n'
    content += '<script src="data-subx_fmc.js"></script>\n'
    content += '<script type="module" src="js-subx_fmc.js"></script>\n'

    page = open("template/stat.html", "r", encoding="utf8").read()
    header = open("template/header.html", "r", encoding="utf8").read() % title
    navbar = open("template/nav_bar.html", "r", encoding="utf8").read()
    explanation = ""
    footer = open("template/footer.html", "r",
                  encoding="utf8").read() % file_name
    closing = open("template/closing.html", "r", encoding="utf8").read()

    with open("pages/%s.html" % file_name, "w", encoding="utf8") as fout:
        fout.write(page %
                   (header, navbar, "", explanation, content, footer, closing))


if __name__ == "__main__":
    main()
