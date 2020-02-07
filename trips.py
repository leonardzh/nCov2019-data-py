import time, json, requests
import pandas as pd

#source: 搜狗
#https://sa.sogou.com/new-weball/page/sgs/epidemic/yyxw?type_page=yangshi&scene=2&clicktime=1580381964&enterid=1580381964&from=timeline&isappinstalled=0
sogou_trips = pd.read_json('https://hhyfeed.sogoucdn.com/js/common/epidemic-search/main.js')
sogou_trips.to_csv('data/trips/sogou_trips.csv')


#source:人民日报
#http://2019ncov.nosugartech.com/search.html?t_date=&t_no=&t_area=
url_trip = 'http://2019ncov.nosugartech.com/data.json?'
json_res = requests.get(url=url_trip).json()['data']
nosugar_trips = pd.DataFrame.from_records(json_res)
nosugar_trips.to_csv('data/trips/nosugar_trips.csv')

#腾讯 https://rl.inews.qq.com/h5/trip?from=newsapp
tx_trip_url = 'https://rl.inews.qq.com/taf/travelFront'
json_res = requests.get(url=tx_trip_url).json()['data']['list']
tx_trips = pd.DataFrame.from_records(json_res)
tx_trips.to_csv('data/trips/tx_trips.csv')