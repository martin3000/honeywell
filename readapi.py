#!/usr/bin/python3
# python3 program getting information from honeywell wifi thermostat
# thru honeywell api
# not for Lyric or round types -> developer.honeywell.com
# (c) 2017 by martin schlatter, schwetzingen, germany

####################### Fill in settings below #######################

USERNAME="mail@domain.com"
PASSWORD="V123"
DOMAIN="mytotalconnectcomfort.com"
APPLID="91db1612-73fd-4500-91b2-e63b069b185c"

############################ End settings ############################

import urllib
import json
import datetime
import http.client
import pprint
    
headers={"Content-Type":"application/json",
         "Accept":"application/json",
         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
        }

body='{"username": "'+USERNAME+'", "password": "'+PASSWORD+'", "applicationId":"'+APPLID+'"}'

conn = http.client.HTTPSConnection(DOMAIN)
conn.request("POST", "/WebApi/api/session",body=body,headers=headers)
r = conn.getresponse()
if r.status==200:
    dict=json.loads(r.read().decode("utf-8"))
    sessionId=dict["sessionId"]
    userID=dict["userInfo"]["userID"]

    headers={"Content-Type":"application/json",
         "Accept":"application/json",
         "sessionId":sessionId,
         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
        }
    conn.request("GET", "/WebApi/api/locations?userId="+str(userID)+"&allData=True",headers=headers)
    r = conn.getresponse()
    if r.status==200:
        dict=json.loads(r.read().decode("utf-8"))
        pprint.pprint(dict)
    else:
        print("could not get locations: ",r.status,r.reason)
else:
    print("could not acquire session id: ",r.status,r.reason)

conn.close()
