# coding=utf-8


import requests
import time,datetime
#import json
#import smtplib
#import hashlib
#import pymysql
#from datetime import datetime


import pandas as pd

N =5
keys = ['牛奶','床',]
#获得即时数据
def get_real_time_data():
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    url = 'https://www.smzdm.com/homepage/json_more?timesort=' + str(c_time) + '&p=1'
    r = requests.get(url=url, headers=headers)

    # data = r.text.encode('utf-8').decode('unicode_escape')
    data = r.text

    dataa = json.loads(data)
    dataa = dataa['data']
    data = pd.DataFrame(dataa)
    data = data[['article_id','article_title','article_price','article_date','article_link']]
    data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #存入文件
    file = data.to_csv('D:/data_1/smzdm.csv',mode='a')
#return data
get_real_time_data()


file_load = pd.read_csv('D:/data_1/smzdm.csv')
#去重
file_load=file_load.drop_duplicates(subset='article_id', keep='first', inplace=False)
#改type
file_load['time'] = pd.to_datetime(file_load['time'], errors ='coerce')
#比较时间
N =5
file_load = file_load[file_load['time'] + datetime.timedelta(days=N) >datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
#查找key

result_titles=[]
for key in keys:
    for title in file_load['article_title']:
        if type(title) is str:
            if title.find(key)!= -1:
                result_titles.append(title) 
#从result_titles中对比之前数据
result_title = pd.DataFrame(result_titles,columns= ['article_title'])
#整合
result =result_title.join(file_load.set_index('article_title'),on='article_title',how='left')
#存入文件
result = result.drop_duplicates(subset='article_id', keep='first', inplace=False)
result = result[['article_title','article_id','article_price','article_date','article_link','time']]
result.to_csv('D:/data_1/smzdm.csv')



fila = pd.read_csv('D:/data_1/smzdm.csv' )
print(fila)


#每5分钟执行一次
for n in range(24):
    for n in range(20):      
        print('开始运行程序')
        get_real_time_data()
        print('结束程序')   
        time.sleep(300)
    fila = pd.read_csv('D:/data_1/smzdm.csv' )
    print(fila)
