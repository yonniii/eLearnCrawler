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
        self.mainView(self.URL + self.mainUri, self.studentNo, self.password)
        self.initSubject(seme)
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

    def initSubject(self,seme):
        self.myLecture(self.getSemester(seme))
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