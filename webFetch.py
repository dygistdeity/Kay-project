import requests
from bs4 import BeautifulSoup

# res = requests.get(
#     "https://pubmed.ncbi.nlm.nih.gov/?term=LYMPHNODES+LYMPHOID+LEUKEMIA%2C+NOS")
res = requests.get(
    "https://pubmed.ncbi.nlm.nih.gov/?term=LIP MUCOEPIDERMOID CARCINOMA SEER")
doc = BeautifulSoup(res.content)

# with open('temp.html', 'w', encoding='utf8') as w:
# w.write(bytes.decode(res.content, encoding='utf-8'))

# from bs4 import BeautifulSoup
# with open('temp.html', 'r', encoding='utf8') as r:
#     soup = BeautifulSoup(r.read())
#     res = soup.find('div', attrs={'class': 'results-amount'})
#     res.find
#     print(type(res))
#     print(res)
#     print(res.content)
#     print(res.contents)
#     print(res.contents[1].string)
