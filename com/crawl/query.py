import pymysql


class DB:
    # db = pymysql.connect(host='ec2-54-180-87-74.ap-northeast-2.compute.amazonaws.com',
    #                      port=3306,
    #                      user='root',
    #                      password='1234',
    #                      db='eLearn',
    #                      charset='utf8')

    def __init__(self, subject, studentNo):
        self.db = pymysql.connect(host='ec2-54-180-87-74.ap-northeast-2.compute.amazonaws.com',
                                  port=3306,
                                  user='root',
                                  password='1234',
                                  db='eLearn',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        self.subject = subject
        self.studentNo = studentNo

    def insertLecture(self, dataList):
        if not dataList or dataList[0] is None:
            print('nonData')
            return None
        sql = """INSERT INTO `eLearn`.`lectures`
(`stdnt_no`,
`id`,
`title`,
`start_time`,
`end_time`,
`type`,
`subject`,
`updated_time`,
`turn`,
`state`,
`runningtime`,
`week`)
VALUES
('%s',
'%s',
'%s',
'%s',
'%s',
'%s',
'%s',
now(),
%d,
'%s',
%s,
%d)
"""
        subSql = """INSERT INTO `eLearn`.`lectures`(`stdnt_no`,`id`,`title`,`start_time`,`end_time`,`type`,`subject`,`updated_time`,`turn`,
        `state`,
        `runningtime`,
        `week`)
        VALUES
        ('%s',
        '%s',DEFAULT,DEFAULT,DEFAULT,
        '%s',
        '%s',
        now(),
        %d,DEFAULT,
        %s,
        %d)
        """
        for data in dataList:
            if not isinstance(data, str):
                # print(week)
                # print(data[3].replace('분',''))
                turn = int(data[0].split()[0])
                id = '%s-%s-%s-%s' % (self.studentNo, self.subject, week, turn)  # 학번,과목,주차,회차 /순서
                id = id.replace(' ', '')
                if self.isExist('lectures', 'id', id):
                    # self.deleteData(data)
                    print("이미 있음")
                    continue
                title = data[2]
                start_time = (data[4])[:16] + ':00'
                end_time = (data[4])[19:] + ':00'
                type = data[1]
                state = data[5]
                if data[3] is '':
                    runningtime = 'null'
                else:
                    runningtime = int(data[3].replace('분', ''))
                # if title is '':
                #     title='null'
                #     start_time='null'
                #     end_time='null'
                #     state='null'

                # id = '%s-%s-%s-%s' % (self.studentNo, self.subject, week, int(data[0].split()[0]))
                # value = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', now() , %d, '%s', %d, %d)" \
                #         % (
                #     self.studentNo, id, data[2],
                #     (data[4])[:14] + ':00', (data[4])[17:] + ':00', data[1], self.subject, data[0].split()[0], data[5],
                #     10, week
                # )
                if not title is '':
                    value = sql % (
                        self.studentNo,
                        id,
                        title,
                        start_time,
                        end_time,
                        type,
                        self.subject,
                        turn,
                        state,
                        runningtime,
                        week
                    )
                else:
                    value = subSql % (
                        self.studentNo,
                        id,
                        type,
                        self.subject,
                        turn,
                        runningtime,
                        week
                    )
                print(value)
                self.executeQuery(value)
            else:
                week = int(data.split()[0])

    def deleteData(self, table, id):
        sql = """DELETE FROM %s WHERE id='%s'""" % (table, id)
        self.executeQuery(sql)

    # data[3].replace('분', '')
    def insertReport(self, dataList):  # timestamp는 now() 쓰셈
        if dataList[0] is None or not dataList:
            print('nonData')
            return None

        sql = """INSERT INTO `eLearn`.`reports`
(`stdnt_no`,
`id`,
`title`,
`start_time`,
`end_time`,
`type`,
`subject`,
`report_no`,
`is_submit`,
`is_include`,
`is_open`,
`fullscore`,
`is_progress`,
`updated_time`)
VALUES
('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', %d, '%s', now())
"""
        for data in dataList:
            report_no = int(data[0])
            id = '%s-%s-%d' % (self.studentNo, self.subject, report_no)
            id = id.replace(' ', '')
            if self.isExist('reports', 'id', id):
                # self.deleteData(data)
                print("이미 있음")
                continue
                ################
            title = data[8]
            start_time = (data[2])[:14] + ':00'
            end_time = (data[2])[17:] + ':00'
            type = data[1]
            is_submit = data[3]
            is_include = data[4]
            is_open = data[5]
            fullscore = int(data[6].replace('점', ''))
            is_progress = data[7]
            value = sql % (
                self.studentNo,
                id,
                title,
                start_time,
                end_time,
                type,
                self.subject,
                report_no,
                is_submit,
                is_include,
                is_open,
                fullscore,
                is_progress
            )
            print(value)
            self.executeQuery(value)

        print(self.cursor.lastrowid)

    def insertNotice(self, dataList, type):
        sql = """INSERT INTO `notices`(`type`, `title`, `url`, `writter`, `date`, `updated_time`) VALUES ('%s','%s','%s','%s','%s',now())"""
        for data in dataList:
            title = data[0]
            url = data[1]
            writter = data[2]
            date = data[3]
            value = sql % (type,
                           title,
                           url,
                           writter,
                           date)
            print(value)
            self.executeQuery(value)

    def isExist(self, table, filde, value):
        sql = """select EXISTS (SELECT * FROM %s WHERE %s = '%s') as success""" % (
            table, filde, value
        )
        print(sql)
        self.executeQuery(sql)
        return self.cursor.fetchone()[0]

    def executeQuery(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
