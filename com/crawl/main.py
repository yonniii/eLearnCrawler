from threading import Thread

from  User import User
from eLearnCrawl import Crawl
from Push import CheckPush
import threading

userGetter = User()
seme = 'spring'

class eleanCrawler(threading.Thread):
    def run(self):
        userList = userGetter.getUser()
        print(userList)
        for user in userList:
            crawler = Crawl(user)
            for i in range(3):
                try:
                    crawler.executeCrawl(seme)
                    break
                except:
                    print('error')


if __name__ =='__main__':
    t1 = eleanCrawler()
    t1.start()

    print("체크시작")
    check = CheckPush()
    check.push()
    print("---the end---")
    t1.join()

    # userList = userGetter.getUser()
    # print(userList)
    # # userList = (('201702040','rmflawy303'),('201701967','981226'),('201702047','981107'))
    # # # userList = ('201701967','981226')
    # # # c = Crawl(('201701967','981226'))
    # # # c.executeCrawl(seme)
    # for user in userList:
    #     crawler = Crawl(user)
    #     for i in range(3):
    #         try:
    #             crawler.executeCrawl(seme)
    #             break
    #         except:
    #             print('error')

