import pymysql

class User:
    def __init__(self):
        self.db = pymysql.connect(host='ec2-54-180-87-74.ap-northeast-2.compute.amazonaws.com',
                                  port=3306,
                                  user='root',
                                  password='1234',
                                  db='eLearn',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def getUser(self):
        sql = 'SELECT * FROM Login WHERE char_length(u_id)=9'
        self.executeQuery(sql)
        return self.cursor.fetchall()

    def executeQuery(self, sql):
        self.cursor.execute(sql)
        self.db.commit()