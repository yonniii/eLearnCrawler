# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests


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

    def parsing(self,url):
        soup = self.getPage(url)
        rows = soup.select('tbody>tr')
        list=[]
        for i in rows:
            data=i.select('td')
            title = data[1].find('a')
            list.append([ " ".join(title.text.split()), url+title['href'], data[3].text,data[4].text])
        print(list)


        # print(rows)

noti = noticeCrawl()
noti.parsing(noti.bachelorURL)
noti.parsing(noti.noticeURL)