import urllib.request
from bs4 import BeautifulSoup
from settings import *

class Speader(object):

    def __init__(self,url):
        self.url = url

    def open_url(self):
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
        req=urllib.request.Request(self.url,headers=headers)
        response=urllib.request.urlopen(req)
        content = response.read()
        html = content
        #html=respond.read().decode('utf-8')
        return html.decode('utf-8')

    def open_img(self):
        fp=urllib.request.urlopen(self.url)
        img = fp.read() 
        return img


def getMedcineFormWeb(urlList):
    id_key = urlList[0]
    each_urlAll =  urlList[1]
    getid = urlList[2]
    jpid = urlList[3]
    lang = urlList[4]
    spead = Speader(each_urlAll)
    html = spead.open_url()
    #html=open_url(each_urlAll)
    soup = BeautifulSoup(html, 'html.parser')
    if lang == 'JP':
        A = soup.find(text="商品名：").findNext('td').text
        B = soup.find(text="　主成分：").findNext('td').text
        C = soup.find(text="　剤形：").findNext('td').text
        D = soup.find(text="　シート記載：").findNext('td').text
        E = str(soup.find(text="　シート記載：").findNext('tr').text)[16:-2]
        F = str(soup.find(text="この薬の作用と効果について").findNext('tr').text)[35:-2]
        G = str(soup.find(text="次のような方は使う前に必ず担当の医師と薬剤師に伝えてください。").findNext('tr').text)[39:-2]
        H = str(soup.find(text="用法・用量（この薬の使い方）").findNext('tr').findNext('tr').text)[40:-2]
        I = str(soup.find(text="生活上の注意").findNext('tr').findNext('tr').text)[28:-2]
        J = str(soup.find(text="この薬を使ったあと気をつけていただくこと（副作用）").findNext('tr').text)[11:-2]
        pic_url = 'http://www.rad-ar.or.jp/siori' + str(soup.find(text='　シート記載：').findNext('img').get('src'))[1:]
    else:
        A = soup.find(text="Brand name :").findNext('td').text
        B = soup.find(text="　Active ingredient:").findNext('td').text
        C = soup.find(text="　Dosage form:").findNext('td').text
        D = soup.find(text="　Print on wrapping:").findNext('td').text
        E = str(soup.find(text="　Print on wrapping:").findNext('tr').text)[27:-2]
        F = str(soup.find(text="Effects of this medicine").findNext('tr').text)[74:-2]
        G = str(soup.find(text="Before using this medicine, be sure to tell your doctor and pharmacist").findNext('tr').text)[47:-2]
        H = str(soup.find(text="Dosing schedule (How to take this medicine)").findNext('tr').findNext('tr').text)[47:-2]
        I = str(soup.find(text="Precautions while taking this medicine").findNext('tr').findNext('tr').text)[46:-2]
        J = str(soup.find(text="Possible adverse reactions to this medicine").findNext('tr').text)[44:-2]
        pic_url = 'http://www.rad-ar.or.jp/siori' + str(soup.find(text='　Print on wrapping:').findNext('img').get('src'))[2:]
    # fp=urllib.request.urlopen(pic_url)
        # img = fp.read() 
    spead_img = Speader(pic_url)
    img = spead_img.open_img()
    medcine = {
        'id':id_key,
        'brand_name':A,
        'ingredient':B,
        'dosage':C,
        'wrapping':D,
        'effects':E,
        'before_using':F,
        'dosing':G,
        'precautions':H,
        'possible':I,
        'stora':J,
        'picture':img,
        'getid':getid,
        'jpid':jpid,
        'lang':lang,
        'creat_by':None,
        'creat_at':None,
        'update_by':None,
        'update_at':None,
    }
    return medcine
    
