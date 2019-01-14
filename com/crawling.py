from urllib.request import urlopen
import bs4


url = "http://computer.cnu.ac.kr/index.php?mid=notice"

html = urlopen(url)

# print(html.read())

bs_Obj = bs4.BeautifulSoup(html.read(), "html.parser")

tbody = bs_Obj.find("tbody")
# print(tbody)

def get_notice():
    tr_notices = tbody.findAll("tr", {"class":"notice"}) #여기까지는 된다..^^ㅎ
    titles = [notice.find("a").find("strong").text for notice in tr_notices]
    for title in titles:
        print(title)

def get_except_notice():
    hxs = tbody.findAll("a", {"class":"hx"})
    for hx in hxs:
        print(hx.text.strip())

print('notice')
get_notice()
print('그냥 글')
get_except_notice()
