from datatool import *
from speader import *
import time
import logging
import logging.config
from settings import *


def getAndSaveToDB(urlList, conn, cs):
    logging.config.fileConfig("log.conf")
    saveOK = False
    medcine = None
    id = urlList[0]
    try:
        medcine = getMedcineFormWeb(urlList)
    except Exception as e:
        logging.error(MESSIG4%(id,urlList[1],e))

    if medcine is not None:
        try:
            saveOK = saveMedcineToDB(medcine, conn , cs)
            if saveOK:
                setGetMedcineStat(id, 2, 0, cs)
                conn.commit()
                logging.info(MESSIG%(urlList[0]))  
        except Exception as e:
            logging.error(MESSIG1%(id,e)) 
            
            saveOK = False
            conn.rollback()

    if not saveOK:
        retry = urlList[6]
        retry += 1
        if urlList[6] < 4:
            setGetMedcineStat(id, 0, retry, cs)
            logging.warning(MESSIG2%(retry))
        else:
            setGetMedcineStat(id, -1, retry, cs)
            logging.error(MESSIG3%(id))
        conn.commit()
        

def main():
    logging.config.fileConfig("log.conf")
    conn = None
    cs = None
    try:
        conn,cs = dbOpen()
        while True:
            urlList = getOnePageToGet(conn, cs)
            if urlList is not None:
                getAndSaveToDB(urlList, conn, cs)
                
                time.sleep(SLEEP_SECONDS)     
            else:
                break
    except:
        pass
    finally:
        dbClose(conn, cs)
    

if __name__ == '__main__':
    main()



