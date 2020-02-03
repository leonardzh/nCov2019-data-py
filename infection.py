import time, json, requests
import pandas as pd

#download data
def downloadDailyData():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    data = json.loads(requests.get(url=url).json()['data'])
    return data

# decode area data to data frame
def getAreaDataFrame(response_data):
    area_tree = response_data['areaTree']
    df_area = pd.DataFrame(columns=['Country','Province','City','AllOrToday','confirm','suspect','dead','heal'])
    for country in area_tree:
        df_area = df_area.append({'Country':country['name'],
                   'Province':'',
                   'City':'',
                   'AllOrToday':'All',
                   'confirm':country['total']['confirm'],
                   'suspect':country['total']['suspect'],
                   'dead':country['total']['dead'],
                   'heal':country['total']['heal']
                  },ignore_index=True)
        df_area = df_area.append({'Country':country['name'],
                   'Province':'',
                   'City':'',
                   'AllOrToday':'Today',
                   'confirm':country['today']['confirm'],
                   'suspect':country['today']['suspect'],
                   'dead':country['today']['dead'],
                   'heal':country['today']['heal']
                  },ignore_index=True)
        if 'children' in country:
            country_tree = country['children']
            for province in country_tree:
                #print('pv:{}'.format(province['name']))
                df_area = df_area.append({'Country':country['name'],
                   'Province':province['name'],
                   'City':'',
                   'AllOrToday':'All',
                   'confirm':province['total']['confirm'],
                   'suspect':province['total']['suspect'],
                   'dead':province['total']['dead'],
                   'heal':province['total']['heal']
                  },ignore_index=True)
                df_area = df_area.append({'Country':country['name'],
                   'Province':province['name'],
                   'City':'',
                   'AllOrToday':'Today',
                   'confirm':province['today']['confirm'],
                   'suspect':province['today']['suspect'],
                   'dead':province['today']['dead'],
                   'heal':province['today']['heal']
                  },ignore_index=True)
                if 'children' in province:
                    province_tree = province['children']
                    for city in province_tree:
                        df_area = df_area.append({'Country':country['name'],
                           'Province':province['name'],
                           'City':city['name'],
                           'AllOrToday':'All',
                           'confirm':city['total']['confirm'],
                           'suspect':city['total']['suspect'],
                           'dead':city['total']['dead'],
                           'heal':city['total']['heal']
                          },ignore_index=True)
                        df_area = df_area.append({'Country':country['name'],
                           'Province':province['name'],
                           'City':city['name'],
                           'AllOrToday':'Today',
                           'confirm':city['today']['confirm'],
                           'suspect':city['today']['suspect'],
                           'dead':city['today']['dead'],
                           'heal':city['today']['heal']
                          },ignore_index=True)
    return df_area

def chinaSummary(data):
    data['chinaTotal']['AllOrToday'] = 'All'
    data['chinaAdd']['AllOrToday'] = 'Today'
    china_summary = pd.DataFrame.from_records([data['chinaTotal'],data['chinaAdd']])
    return china_summary

def getHistory(data):
    china_history_sum = pd.DataFrame.from_records(data['chinaDayList'])
    china_history_add = pd.DataFrame.from_records(data['chinaDayAddList'])
    return china_history_sum, china_history_add

def saveAll(data):
    last_time = data['lastUpdateTime'].replace(':','-')
    area_df = getAreaDataFrame(data)
    area_df.to_csv('data/infections/area_{}.csv'.format(last_time),index=False)
    summary = chinaSummary(data)
    summary.to_csv('data/infections/summary_{}.csv'.format(last_time),index=False)
    history_sum,history_add = getHistory(data)
    history_sum.to_csv('data/infections/history_sum_{}.csv'.format(last_time),index=False)
    history_add.to_csv('data/infections/history_add_{}.csv'.format(last_time),index=False)

# Run this function daily to save data
def updateNow():
    data = downloadDailyData()
    saveAll(data)
    return data
