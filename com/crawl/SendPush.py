import requests
import json

class SendPush:
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


ids = 'e_yTrAZmLBg:APA91bH_niAX51L10gLi1iXMccpNGjF9XfI34Xws_TnNAsb62r9FaF2iV2IE3eq_ISe4VoH5Irom6pAAIoNP1PWLV4EnnMtesIkBl_2bnqHTqjs5EJHgU897Q-W4gR7LhgmGoj04aFVL'
title = 'test'
body = 'please'
send = SendPush()
send.sendFcmNotification(ids,title,body)