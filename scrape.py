import requests
import json
from bs4 import BeautifulSoup as bs
import re


def cleanup_structure():
    json.dump({i["nodeid"]: {
        "title": i["nodetitle"],
        "sections": {i["itemid"]: {
            "title": i["title"],
            "subsections": {
                i["id"]: i["title"] for i in i["coursepages"]
            }
        } for i in i["items"]}
    } for i in structure["chapters"]}, open("course_structure.json", "w"), indent=4, ensure_ascii=False)


# cleanup_structure()


def scrape():
    structure = json.load(open("course_structure.json", "r"))

    for id, content in list(structure.items()):
        data = {}
        while True:
            try:
                content = requests.get("https://api.ulearning.asia/wholepage/chapter/stu/"+id, headers={
                    "UA-AUTHORIZATION": "5608DEF69F7485CE2E5B520655221E07",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
                }, timeout=5).json()
                break
            except:
                pass

        chapterId = str(content["chapterid"])
        chapterTitle = structure[chapterId]["title"]
        data[chapterTitle] = {}

        for section in content["wholepageItemDTOList"]:
            sectionId = str(section["itemid"])
            sectionTitle = structure[chapterId]["sections"][sectionId]["title"]
            data[chapterTitle][sectionTitle] = {}

            for subsection in section["wholepageDTOList"]:
                subsectionId = str(subsection["id"])
                subsectionTitle = structure[chapterId]["sections"][sectionId]["subsections"][subsectionId]

                rawContent = subsection["coursepageDTOList"][0]["content"]
                innerContent = bs(rawContent, "html.parser").text

                data[chapterTitle][sectionTitle][subsectionTitle] = re.sub(r"\$\{.*?\}", "", re.sub(
                    r"\s{4,}", "\n", innerContent).strip())

        json.dump(data, indent=4, ensure_ascii=False,
                  fp=open(chapterTitle+".json", "w"))

        print("Done ", chapterTitle)
