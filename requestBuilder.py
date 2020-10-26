import json
from sys import exec_prefix
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
    worksheet.write(0, 5, label='url of req.keyI req.keyII SEER')
    worksheet.write(0, 6, label="req.keyI req.keyII SEER")
    worksheet.write(0, 7, label="req.keyI req.keyII")
    worksheet.write(0, 8, label="req.keyII SEER")
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
                worksheet.write(
                    count, 5, label=f"https://pubmed.ncbi.nlm.nih.gov/?term={res.keyI} {res.keyII} SEER")
                for i in range(len(res.resList)):
                    worksheet.write(count, i+6, label=res.resList[i])
                print(f"[{titleI['key']} {titleII['key']} SEER] 搜索成功")
            else:
                print(f"[{titleI['key']} {titleII['key']} SEER] 搜索出错")
                err += 1
            count = count+1
            if(count % 3 == 0):
                try:
                    workbook.save('搜索结果.xls')
                    print("中断点：已保存到文件")
                except Exception as e:
                    print("文件保存失败，放弃保存中断点")
    print(f"总共 {count} 次搜索，失败 {err} 次")
    workbook.save('搜索结果.xls')


def fetch(req: SearchResult) -> SearchResult:
    req.resList = []
    req.search_content = [
        f"{req.keyI} {req.keyII} SEER",
        f"{req.keyI} {req.keyII}",
        f"{req.keyII} SEER",
    ]
    for i in req.search_content:
        print(f"正在搜索 {i}", end="\r")
        req.resList.append(countOfResult(
            f"https://pubmed.ncbi.nlm.nih.gov/?term={i}"))
    return req


def countOfResult(url):
    try:
        res = requests.get(url)
        # content = bytes.decode(res.content, encoding='utf8')
        soup = BeautifulSoup(res.content)
        contents = soup.find('div', attrs={'class': 'results-amount'})
        if contents == None:
            if soup.find('div', attrs={'class': 'single-result-redirect-message'}):
                return 1
            if soup.find('div', attrs={'class': 'return-to-search'}):
                return 1
        contents = contents.contents
        if len(contents) == 1:
            return 0
        rawInt = soup.find(
            'div', attrs={'class': 'results-amount'}).contents[1].string
        strInt = ""
        for i in rawInt.split(","):
            strInt += i
        return int(strInt)
    except Exception as e:
        print(f"访问{url}出错：错误类型{e}")
        return None


if __name__ == '__main__':
    build()
