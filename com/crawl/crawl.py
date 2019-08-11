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


