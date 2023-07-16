import os
import json


def convertToMarkdown():
    for i in os.listdir("./json"):
        if i.endswith(".json"):
            markdown = ""
            data = json.load(open("./json/"+i, "r"))

            for chapter, sections in data.items():
                markdown += "## "+chapter+"\n"
                for section, subsections in sections.items():
                    markdown += "### "+section+"\n"
                    for subsection, content in subsections.items():
                        markdown += "#### "+subsection+"\n"
                        markdown += content+"\n\n"

        open("./markdown/" + i.split(".")[0]+".md", "w").write(markdown)


convertToMarkdown()

continents = {}
for country in os.listdir("./markdown"):
    continentData = json.load(open("./continents.json", "r"))
    mapping = [i for i in continentData if i["country_cname"] == country.split(".")[
        0]]
    if (mapping):
        mapping = mapping[0]
        if mapping["continent_cname"] not in continents:
            continents[mapping["continent_cname"]] = []
        continents[mapping["continent_cname"]].append(country)

for continent, countries in continents.items():
    markdown = "# "+continent+"\n\n"

    for country in countries:
        markdown += open("./markdown/"+country, "r").read()
        os.remove("./markdown/"+country)

    open("./markdown/"+continent+".md", "w").write(markdown + "\n\n")
