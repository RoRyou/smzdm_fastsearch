# coding=utf-8
import requests
import random
import re
import time,datetime
import calendar
import pandas as pd

keyword = '洗衣机'
time = datetime.datetime.now()
lasttime = time -datetime.timedelta(days=3)
refresh_time = 3
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

r = requests.get('http://feed.smzdm.com', headers=headers, timeout=random.random() + random.randint(1, 2))

title = re.findall(r'<title>(.*?)</title>', r.text)
link = re.findall(r'<link>(.*?)</link>', r.text)
pubDate =re.findall(r'<pubDate>(.*?)</pubDate>', r.text)

output_data,output_link = [],[]
for n in range(refresh_time):
    for n in title:
        if keyword in n:
            #title.index(n)   为编号
            D_time, m_time, Y_time, H_time, M_time, S_time = pubDate[1][14:16], pubDate[1][17:20], pubDate[1][21:25], \
                                                             pubDate[1][26:28], pubDate[1][29:31], pubDate[1][32:34],
            m_time = list(calendar.month_abbr).index(m_time)
            thistime = datetime.datetime(int(Y_time),m_time,int(D_time))
            print('-----')
            if lasttime < thistime:
                print(n[9:-3])
                #print(title.index(n))
                print(link[title.index(n)][17:-3])
                output_data.append(n[9:-3])
                output_link.append(link[title.index(n)][17:-3])


print(output_data)
output_data = pd.DataFrame(output_data)
output_link = pd.DataFrame(output_link)

output = output_data+output_link




