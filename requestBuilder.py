import json
from bs4 import BeautifulSoup
import requests
import xlwt


class SearchResult(json.JSONEncoder):
    # 访问URL
    url: str = None
    # 搜索评分
    resList: list = list()
    # 搜索关键词
    search_content: str
    # 一级标题
    keyI: str
    # 一级代码
    codeI: str
    # 二级标题
    keyII: str
    # 二级代码
    codeII: str

    def __init__(self, keyI, codeI, keyII, codeII):
        self.keyI = keyI
        self.codeI = codeI
        self.keyII = keyII
        self.codeII = codeII


def build():
    count = 1
    err = 0
    data_dict = None
    res_list = list()
    with open('data.json', 'r', encoding="utf8") as r:
        data_dict = json.load(r)
    if data_dict is None:
        return
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('搜索结果')
    worksheet.write(0, 0, label='搜索内容')
    worksheet.write(0, 1, label='keyI')
    worksheet.write(0, 2, label='keyII')
    worksheet.write(0, 3, label='codeI')
    worksheet.write(0, 4, label='codeII')
    worksheet.write(0, 5, label='score')
    for titleI in data_dict:
        for titleII in titleI['sub']:
            print(f"[{titleI['key']} {titleII['key']} SEER] 搜索中", end='\r')
            itemResult = SearchResult
            res = fetch(SearchResult(
                titleI['key'], titleI['code'], titleII['key'], titleII['code']))
            if res.resList != None:
                res_list.append({'score': res.resList, 'keyI': res.keyI,
                                 'keyII': res.keyII, 'codeI': res.codeI, 'codeII': res.codeII, 'content': res.search_content})
                worksheet.write(count, 0, label=res.search_content)
                worksheet.write(count, 1, label=res.keyI)
                worksheet.write(count, 2, label=res.keyII)
                worksheet.write(count, 3, label=res.codeI)
                worksheet.write(count, 4, label=res.codeII)
                worksheet.write(count, 5, label=res.resList)
                count += 1
                print(f"[{titleI['key']} {titleII['key']} SEER] 搜索成功")
            else:
                print(f"[{titleI['key']} {titleII['key']} SEER] 搜索出错")
                err += 1
    print(f"总共 {count} 次搜索，失败 {err} 次")
    workbook.save('搜索结果.xls')
    with open('webResult.json', 'w', encoding='utf8') as w:
        json.dump(res_list, w)


def fetch(req: SearchResult) -> SearchResult:
    content = None
    fileName = None
    try:
        req.search_content = f"{req.keyI} {req.keyII} SEER"
        req.url = f"https://pubmed.ncbi.nlm.nih.gov/?term={req.search_content}"
        fileName = req.search_content
        res = requests.get(req.url)
        content = bytes.decode(res.content, encoding='utf8')
        soup = BeautifulSoup(res.content)
        contents = soup.find('div', attrs={'class': 'results-amount'})
        if contents == None:
            if soup.find('div', attrs={'class': 'single-result-redirect-message'}):
                req.resList = 1/2
                return req
        contents = contents.contents
        if len(contents) == 1:
            req.resList = 1
            return req
        req.resList = 1/(1+int(
            soup.find('div', attrs={'class': 'results-amount'}).contents[1].string))
        return req
    except Exception as e:
        with open(f"{fileName}.html", 'w', encoding='utf8') as w:
            w.write(content)
        print()
        print(e)
        return req
    return req


if __name__ == '__main__':
    build()
