# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 19:35:23 2018

@author: ryx14
"""
#
import requests
import re
import json
import datetime
import pytz
import pandas as pd
tz = pytz.timezone('Asia/Shanghai')
today = datetime.datetime.now(tz).date()
day = today + datetime.timedelta(7)
end_info_day = today + datetime.timedelta(14)
end_insurance_day = today + datetime.timedelta(180)
flight_info_source=[]
while day <= end_info_day:
    Params = {"date": str(day), "lang": "zh_CN", "cargo": "false", "arrival": "false"}
    r = requests.get("https://www.hongkongairport.com/flightinfo-rest/rest/flights", params=Params)
    day = day + datetime.timedelta(1)
    lst = json.loads(r.text)[0]['list']
    for d in lst:
        destination = ''
        for dest in d['destination']:
            destination += (dest+'/')
        destination = destination[:-1]
        for f in d['flight']:
            l = [f['no'],destination]
            if not l in flight_info_source:
#                l = l + [str(day),d['time']]
                flight_info_source += [l]
#        destination = d['destination']
#        destination.sort()
#        airlines = [f['no'] for f in d['flight']]
#        airlines.sort()
#        l = [destination, airlines]
#        if not l in flight_info_source:
#            l = l + [str(day),d['time']]
#            flight_info_source += [l]
columns = ['Flight Number','Destination']
day = today + datetime.timedelta(7)
while day <= end_insurance_day:
    columns += [str(day)]
    date = str(day).split('-')
    date = date[1] + '/' + date[2] + '/' +date[0]
    for i in range(len(flight_info_source)):
        flightnumber = flight_info_source[i][0]
        Params = {"planCode": "FlightDelay", "referralCode": "", "flightNo": flightnumber, "date": date}
        r = requests.get("https://i.fwd.com.hk/fwdhkapi/api/flightDelay/quotes", params=Params)
        pattern = '"originalPrice":(.*),"totalDue"'
        if "originalPrice" in r.text:
            price = re.findall(pattern, r.text)[0]
            price = 'HK$' + price
        else:
            price = 'Not offered'
        flight_info_source[i] = flight_info_source[i] + [price]
df=pd.DataFrame(flight_info_source,columns=columns)
df.to_csv('task6.csv')