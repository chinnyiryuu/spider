import urllib.request
import re
import pymysql
from bs4 import BeautifulSoup
import datetime
import time

def open_url(url):
    headers ={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"ja,en-US;q=0.8,en;q=0.6",
            "Connection":"keep-alive",
            #"Cookie":"__utmz=229506719.1504243626.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __utma=229506719.764529420.1504243626.1504243626.1504246950.2; __utmc=229506719; session=BSrogyvkY8R; __utmb=229506719; _ga=GA1.3.1725688705.1504243625; _gid=GA1.3.226221163.1504243625",
            "Host":"www.rad-ar.or.jp",
            "Referer":"http://www.rad-ar.or.jp/siori/kensaku.cgi?mode=wa&wa1=0",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            }
    req=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(req)
    content = response.read()
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(content, 16+zlib.MAX_WBITS)
    else:
        html = content
    #html=respond.read().decode('utf-8')
    return html.decode('utf-8')

def get_url(url):
    sums = []
    count = 0
    html=open_url(url)
    time.sleep(0.5)
    conn = pymysql.connect(host="localhost",port=3306,user="root",passwd="chen",db="test", charset="utf8")
    c=conn.cursor()
    add_sql = ("INSERT INTO url_mast(url,getid,get_state,jpid,lang,creat_by,creat_at,update_by,update_at)"
                " VALUES (%(url)s,%(getid)s,%(get_state)s,%(jpid)s,%(lang)s,%(creat_by)s,%(creat_at)s,%(update_by)s,%(update_at)s)")
    soup = BeautifulSoup(html, 'html.parser')
    Num = str(soup.find("p", attrs={"class": "resultsNum"}).text)[4:-1]
    resultsNum = int(Num)
    sums.append(resultsNum)
    soup.find("p", attrs={"class": "resultsNum"}).text
    for k in soup.find_all('h2',class_='blockLink'):
        a = k.find_all('a')
        #print(a[0])
        b = str(a[0]).split('"')
        d = str(b[1]).split('=')
        #print(b)
        each_url = "http://www.rad-ar.or.jp" + b[1]
        getid = int(d[1])
        
        date_sql = {
        'url':each_url,
        'getid':getid,
        'get_state':0,
        'jpid':None,
        'lang':'JP',
        'creat_by':'spead',
        'creat_at':datetime.datetime.now(),
        'update_by':'spead',
        'update_at':datetime.datetime.now(),
        }
        try:
            c.execute(add_sql,date_sql)
            count += 1
            #conn.commit()
        except :  
            conn.rollback()
        c.execute("SELECT @@IDENTITY")
        row = c.fetchall()
        if soup.find("a", attrs={"href": b[1]}).findNext('a').text == '英語版あり':
            L=soup.find("a", attrs={"href": b[1]}).findNext('a')
            b = str(L).split('"')
            d = str(b[1]).split('=')
            each_url = "http://www.rad-ar.or.jp" + b[1]    
            date_sql = {
            'url':each_url,
            'getid':int(d[1]),
            'get_state':0,
            'jpid':row,
            'lang':'UK',
            'creat_by':'spead',
            'creat_at':datetime.datetime.now(),
            'update_by':'spead',
            'update_at':datetime.datetime.now(),
            }
            try:
                c.execute(add_sql,date_sql)
                count += 1
            except :  
                conn.rollback()
    
    conn.commit()
    c.close()
    conn.close()
    sums.append(count)
    return sums


for i in range(5,10):
    coun=0
    a = 5
    if i == 7 or i == 9:
        a = 3
     for j in range(a):
        if j == 0:
            url='http://www.rad-ar.or.jp/siori/kensaku.cgi?mode=wa&wa1=' + str(i)
        else:
            url='http://www.rad-ar.or.jp/siori/kensaku.cgi?wa2=' + str(j)
        sums = get_url(url)
        coun += sums[1]
        #print('有%d行数据被插入'%coun)
        for sumon in range(2,(sums[0]//25)+2):
            url = 'http://www.rad-ar.or.jp/siori/kensaku.cgi?page=' + str(sumon)
            sumse = get_url(url)
            coun += sums[1]
            #print('有%d行数据被插入'%coun)
    print('共有%d行数据被插入'%coun)
    print(i)
    