import urllib.request
import re
import pymysql
from bs4 import BeautifulSoup
#爬取整个网页的方法
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

#爬取每个页面中每一个药品对应的链接
def get_url_list(url):
    html=open_url(url)
    url_list=[]
    soup = BeautifulSoup(html, 'html.parser')
    for k in soup.find_all('h2',class_='blockLink'):
        a = k.find_all('a')
        #print(a[0])
        b = str(a[0]).split('"')
        c = str(b[1]).split('=')
        print(c[1])
        url_list.append(b[1])
    #p=re.compile(r'<h2 class="blockLink"><a href=".+?n=.+">')
    #url_list=re.findall(p,html)
    return url_list

#自动进入每一个药品对应的链接中爬取每一张图片对应的链接并插入到mysql数据库
def get_img(url):
    #获取每个页面中每一个药品对应的链接
    url_list=get_url_list(url)
    #连接mysql数据库
    #conn = pymysql.connect(host="localhost",port=3306,user="root",passwd="chen",db="test" )
    #conn=connect(user='root',password='chen',database='test')
    #创建游标
    #c=conn.cursor()
    #try:
        #创建一张数据库表
        #c.execute('create table chemicals(name varchar(30) ,img varchar(100))')
    #except:
        #count用来计算每一张网页有多少行数据被插入
    #    count=0
    for each_url in url_list: 
        each_urlAll =  "http://www.rad-ar.or.jp" + each_url
        html=open_url(each_urlAll)
        soup = BeautifulSoup(html, 'html.parser')
        for k in soup.find_all('div',class_='bn'):
            print(k)
            
        #p1=re.compile(r'<td width="30%" align="center" valign="middle"><img alt src="(.+)" border="0"></td>')
        #p2=re.compile(r'<div class="bn">(.+)</div>')
        #img_list=re.findall(p1,html)
        #title=re.findall(p2,html)
        #for each_img in img_list:
            #c.execute('insert into cartoon values(%s,%s)',["15453",each_img])
            #count+=c.rowcount
    #print('有%d行数据被插入'%count)

    #finally:
    #    conn.commit()
    #    c.close()
    #    conn.close()
           
for i in range(9):
    url='http://www.rad-ar.or.jp/siori/kensaku.cgi?mode=wa&wa1='+str(i+1)
    get_img(url)