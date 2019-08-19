# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
from query import DB


class noticeCrawl:
    def __init__(self):
        self.bachelorURL = 'https://computer.cnu.ac.kr/computer/notice/bachelor.do'
        self.noticeURL='https://computer.cnu.ac.kr/computer/notice/notice.do'
        self.projectURL='https://computer.cnu.ac.kr/computer/notice/project.do'
        self.jobURL='https://computer.cnu.ac.kr/computer/notice/job.do'
        self.cseURL = 'https://computer.cnu.ac.kr/computer/notice/cse.do'

    def getPage(self,url):
        req = requests.get(url)
        html = req.text
        return BeautifulSoup(html, 'html.parser')

    def getURL(self,type):
        if type=='barchelor':
            return self.bachelorURL
        elif type=='notice':
            return self.noticeURL
        elif type=='project':
            return self.projectURL
        elif type=='job':
            return self.jobURL
        elif type =='cse':
            return self.cseURL

    def parsing(self,type):
        url = self.getURL(type)
        soup = self.getPage(url)
        rows = soup.select('tbody>tr')
        list=[]
        for i in rows:
            data=i.select('td')
            num = data[0].text.strip()
            title = data[1].find('a')
            titleTxt = " ".join(title.text.split())
            titleTxt = titleTxt.replace("'","")
            print(titleTxt)
            list.append([ titleTxt, url+title['href'], data[3].text,data[4].text,num])
        # print(list)
        db = DB(None,None)
        db.insertNotice(list,type)

list = ['barchelor','notice','project','job','cse']
noti = noticeCrawl()
for i in list:
    noti.parsing(i)