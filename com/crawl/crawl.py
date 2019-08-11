# -*- coding:utf-8 -*-
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from enum import Enum
from query import DB
import enum

class Crawl:
    def __init__(self, studentNo, password):
        self.studentNo = studentNo
        self.password = password
        self.subject = {}
        self.URL = 'http://e-learn.cnu.ac.kr'
        self.mainUri = '/main/MainView.dunet'
        # myLectureUri= '/lms/myLecture/doListView.dune'
        self.myLectureUri = '/lms/myLecture/doListView.dunet?mnid=201008840728'
        self.reportUri = '/lms/class/report/stud/doListView.dunet'
        self.courseUri = '/lms/class/courseSchedule/doListView.dunet'
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=ko_KR')
        self.driver = webdriver.Chrome('C:/chromedriver/chromedriver', chrome_options=chrome_options)
        self.driver.implicitly_wait(3)


    def main(self,seme):
        self.seme = seme
        self.mainView(self.URL + self.mainUri, self.studentNo, self.password)
        self.initSubject()
        self.crawlSubject()

    def mainView(self,url, id, password):
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_xpath('//*[@id="pop_login"]').click()
        self.driver.find_element_by_name('id').send_keys(id)  # 학번
        self.driver.find_element_by_name('pass').send_keys(password)  # 비번
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//*[@id="login_img"]').click()
        time.sleep(2)

    def initSubject(self):
        self.myLecture(self.getSemester(self.seme))
        i = 0
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for assign in soup.select("a.classin2"):
            sub = assign.text.strip()
            title = sub[0:(len(sub) - 14)]
            # num = sub[(len(sub)-12):len(sub)-1]
            self.subject[title] = i
            i = i + 1
            print(self.subject[title])

    def myLecture(self,semester):
        self.driver.get(self.URL + self.myLectureUri)
        # driver.find_elements(By.CLASS_NAME, 'btn_menu_link.on').click()
        # driver.find_element(By.linkText("나의강의실")).click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//select[@name="term_cd"]/option[@value = "%s"]' % semester).click()  # 학기 선택
        self.driver.find_element_by_xpath('//*[@id="ing"]').click()

    def getSemester(self,semester):
        seme =semester
        if seme is 'spring':
            return 10
        elif seme is 'summer':
            return 11
        elif seme is 'fall':
            return 20
        elif seme is 'winter':
            return 21
        elif seme is 'normal':
            return 00
        return 10

    def crawlSubject(self):
        for i in self.subject.keys():
            print(i)
            self.selectLecture(self.subject[i])
            self.getReport(i)
            time.sleep(5)
            self.getCourse(i)

    def selectLecture(self,lectureNo):
        self.myLecture(self.getSemester(self.seme))
        self.driver.implicitly_wait(3)
        classes = self.driver.find_elements(By.CLASS_NAME, 'classin2')
        classes[lectureNum].click()
        time.sleep(1)

    def getReport(self,subject):
        self.driver.get(self.URL + self.reportUri)
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        parse = Parser(subject)
        parsedData = parse.parsing(soup.select('.datatable.mg_t10.fs_s'), 0)
        db = DB(subject, self.studentNo)
        db.insertReport(parsedData)
        time.sleep(2)

    def getCourse(self,subject):
        self.driver.get(self.URL + self.courseUri)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        parse = Parser(subject)
        parsedData = parse.parsing(soup.select('.datatable.mg_t10.fs_s.bo_rn'), 1)
        # if not parsedData or (parsedData[0] is None):
        #     print("데이터 없더라")
        # else:
        db = DB(subject, self.studentNo)
        db.insertLecture(parsedData)
        time.sleep(2)

class Parser:
    reportColumns = ['num', 'type', 'period', 'isSubmit', 'isInclude', 'isOpen', 'fullScore', 'isProgress', 'title']
    lectureColumns = ['turn', 'type', 'title', 'time', 'period', 'state']
    subject =''

    def __init__(self,subject):
        self.subject= subject

    def parsing(self, data, dataType):
        rawData = data[0].find("tbody").find_all("tr")  ##공통
        list = []
        if dataType == 0:
            list = self.insertParsedData(rawData, self.parseReportData)
        elif dataType == 1:
            list = self.insertParsedData(rawData, self.parseLectureData)  #
        print(list)
        return list

    def insertParsedData(self, data, parse):
        list = []
        for i in data:
            list.append(parse(i))
        return list

    def parseReportData(self, data):

        if data.find(colspan='7') is not None:
            return
        tac = data.select(".ta_c")
        tal = data.select(".ta_l")

        report_item0 = tac[0].text
        report_item1 = tac[1].text
        report_item2 = tac[2].text.strip()
        report_item3 = tac[3].text.strip()
        report_item4 = tac[4].text.strip()
        report_item5 = tac[5].text.strip()
        report_item6 = tac[6].text
        report_item7 = tac[7].text.strip()
        report_item8 = tal[0].text.strip()

        report_item= [report_item0, report_item1, report_item2, report_item3, report_item4, report_item5, report_item6,
             report_item7, report_item8]

        # columns = ['num', 'type', 'period','isSubmit', 'isInclude','isOpen', 'fullScore','isProgress', 'title']

        # table = {}
        # table['num'] = tac[0].text
        # table['type'] = tac[1].text
        # table['period'] = tac[2].text.strip()
        # table['isSubmit'] = tac[3].text.strip()
        # table['isInclude'] = tac[4].text.strip()
        # table['isOpen'] = tac[5].text.strip()
        # table['fullScore'] = tac[6].text
        # table['isProgress'] = tac[7].text.strip()
        # table['title'] = tal[0].text.strip()
        # return table

        return report_item

    def parseLectureData(self, data):
        if data.find(colspan='8') is not None:
            tmp = " ".join(data.text.split())
            # c = tmp.find('\n')
            # if not(c is -1):
            #     tmp=tmp[:c]
            # return {tmp[0]:tmp}
            return tmp
        else:
            td = data.select('td')

            lecture_item0 = data.select('th')[0].text
            lecture_item1 = td[0].text.strip()
            lecture_item2 = " ".join(td[1].text.split())
            lecture_item3 = td[2].text.strip()
            lecture_item4 = td[3].text.strip()
            lecture_item5 = td[4].text.strip()

            lecture_item = [lecture_item0, lecture_item1, lecture_item2, lecture_item3, lecture_item4, lecture_item5 ]


            # table = {}
            # table['turn'] = data.select('th')[0].text
            # td = data.select('td')
            # table['type'] = td[0].text.strip()
            # table['title'] = td[1].text.strip()
            # table['time'] = td[2].text.strip()
            # table['period'] = td[3].text.strip()
            # table['state'] = td[4].text.strip()
            # return table
            return lecture_item
