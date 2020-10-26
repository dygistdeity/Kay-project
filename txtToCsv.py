import re
import json
dataDict = list()
titleI = None
titleII = None
with open("src.txt", 'r', encoding='UTF8') as r:
    for i in r.readlines():
        res = re.match("^([A-Z][A-Z ]+)\s(C.*)\s*", i)
        if (res != None and titleI != i):
            dataDict.append({
                "key": res.group(1),
                "code": res.group(2),
                "sub": list()
            })
            print(f"一级标题: {res.group(1)}\t代码: {res.group(2)}")
            titleI = i
            titleII = None
            continue 
        res = re.match("^\t([A-Z][A-Z.,&\-/\\ ]+)\s*(\d{3})\s*", i)
        if (res != None and titleII != i):
            dataDict[-1]["sub"].append({
                "key": res.group(1),
                "code": res.group(2),
                "sub": list()
            })
            print(f"\t二级标题: {res.group(1)}\t代码: {res.group(2)}")
            titleII = i
            continue
        res = re.match("^\t\t(\d{4}/\d)\s*(.*)\s*", i)
        if (res != None):
            dataDict[-1]["sub"][-1]["sub"].append({
                "key": res.group(2),
                "code": res.group(1)
            })
            print(f"\t\t三级标题: {res.group(2)}\t代码: {res.group(1)}")
with open("data.json", "w", encoding="UTF8") as w:
    json.dump(dataDict, w)
