from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time,httplib

today =  getBeijinTime()
str_today = str(today)
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
SchoolDay = os.environ['SCHOOLDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
template_id = os.environ["TEMPLATE_ID"]

def getBeijinTime():
   try:
     conn = httplib.HTTPConnection("www.beijing-time.org")
     conn.request("GET", "/time.asp")
     response = conn.getresponse()
     print response.status, response.reason
     if response.status == 200:
       result = response.read()
       data = result.split("\r\n")
       year = data[1][len("nyear")+1 : len(data[1])-1]
       month = data[2][len("nmonth")+1 : len(data[2])-1]
       day = data[3][len("nday")+1 : len(data[3])-1]
       #wday = data[4][len("nwday")+1 : len(data[4])-1]
       hrs = data[5][len("nhrs")+1 : len(data[5])-1]
       minute = data[6][len("nmin")+1 : len(data[6])-1]
       sec = data[7][len("nsec")+1 : len(data[7])-1]
       beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
       beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
       return beijinTim

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days
def get_SchoolDay():
  next = datetime.strptime(str(date.today().year) + "-" + SchoolDay, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"datatime":{"value":str_today},"SchoolDay":{"value":get_SchoolDay()},"city":{"value":city},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1, template_id, data)
print(res1)
print(res)
