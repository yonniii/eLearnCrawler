import requests
import json
import pymysql


class Push:
    def sendFcmNotification(self,ids,title,body):
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': 'key=AAAAEMqRNFQ:APA91bHaHAtURfCvzQ1w7PtsjLwS963_-2FKElT2hllqSPCcrQ7yez2HFiDf7QGHqWV496CSqGVhRtyawE0vXIWaO4Nm_McJ5SSR3eJ4iRX6-33pbmNz6yympa7ajQrjvAlsVEJpbZKr',
            'Content-Type': 'application/json; UTF-8',
        }
        content = {
            'to': ids,
            'notification': {
                'title': title,
                'body': body
            }
        }
        requests.post(url, data=json.dumps(content), headers=headers)





class CheckPush:
    def __init__(self):
        self.db = pymysql.connect(host='ec2-54-180-87-74.ap-northeast-2.compute.amazonaws.com',
                                  port=3306,
                                  user='root',
                                  password='1234',
                                  db='eLearn',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def timeDiff(self, table, intval, type):
        intervalListsql = """SELECT * FROM `%s` WHERE `is_submit`='미제출' and `end_time` BETWEEN DATE_ADD(NOW(),INTERVAL %d %s) AND DATE_ADD(NOW(),INTERVAL %d %s)""" % (
        table, intval, type, intval+1, type)
        # ss = """SELECT * FROM `reports` WHERE `end_time` BETWEEN DATE_ADD(NOW(),INTERVAL 1 DAY) AND DATE_ADD(NOW(),INTERVAL 2 DAY)"""
        self.executeQuery(intervalListsql)
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def pushDue(self):
        ids = 'e_yTrAZmLBg:APA91bH_niAX51L10gLi1iXMccpNGjF9XfI34Xws_TnNAsb62r9FaF2iV2IE3eq_ISe4VoH5Irom6pAAIoNP1PWLV4EnnMtesIkBl_2bnqHTqjs5EJHgU897Q-W4gR7LhgmGoj04aFVL'
        push = Push()
        list = self.timeDiff('reports',1,'day')
        for i in list:
            title = i[1] + ' 마감 1일 전'
            body = i[1] + ' 마감 1일 전'
            push.sendFcmNotification(ids, title, body)

    def pushNewNotice(self,data):
        ids = 'e_yTrAZmLBg:APA91bH_niAX51L10gLi1iXMccpNGjF9XfI34Xws_TnNAsb62r9FaF2iV2IE3eq_ISe4VoH5Irom6pAAIoNP1PWLV4EnnMtesIkBl_2bnqHTqjs5EJHgU897Q-W4gR7LhgmGoj04aFVL'
        push = Push()
        title = '[새 공지 알림]'
        body =data[0]
        push.sendFcmNotification(ids, title, body)

    def executeQuery(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

# ids = 'e_yTrAZmLBg:APA91bH_niAX51L10gLi1iXMccpNGjF9XfI34Xws_TnNAsb62r9FaF2iV2IE3eq_ISe4VoH5Irom6pAAIoNP1PWLV4EnnMtesIkBl_2bnqHTqjs5EJHgU897Q-W4gR7LhgmGoj04aFVL'
# title = 'test'
# body = 'please'
# push = Push()
# # push.sendFcmNotification(ids, title, body)
#
# ch = CheckPush()
# list = ch.timeDiff('reports',1,'day')
# for i in list:
#     title = i[1]+' 마감 1일 전'
#     body = i[1]+' 마감 1일 전'
#     push.sendFcmNotification(ids, title, body)
