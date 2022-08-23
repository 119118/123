from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
#接下来五步更换为自己女朋友的信息即可
start_date = "2018-03-16"  #恋爱开始时间
city = "101220101"         #城市天气查询的id ,根据自己城市上网查询即可,当前是合肥市
birthday = "06-06"         #出生日期
app_id = "wxb1e5385c50a7af37" #微信测试的app_id
app_secret = "0a8589fbe9e7fefcbcb49c9be4ece657" #微信测试的app_secret
user_id = "oJjoj56DH_yxUozWHtTScDlCdzOo"        #扫码生成的user_id(女朋友的user_id)
template_id = "KwlL2kXjjyxdGw-ey0UpZxgNKV8UvKfjy6qdnwLggOY" #生成的模板id


def get_weather():
  # url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  url = "http://t.weather.sojson.com/api/weather/city/" + city
  res = requests.get(url).json()
  # weather = res['data']['list'][0]
  weather = res['data']
  return weather['quality'], weather['wendu']
  # return weather['quality'], math.floor(weather['wendu'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
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
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
