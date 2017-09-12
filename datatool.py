import pymysql
import datetime
from settings import *

def dbOpen():
    conn = pymysql.connect(host="localhost",port=3306,user="root",passwd="chen",db="test", charset="utf8")
    cs = conn.cursor()
    return (conn,cs)

def dbClose(conn,cs):
    if cs is not None:
        cs.close()
    if conn is not None:
        conn.close()

def getUrl(sql_one):
    conn,cs = dbOpen()
    try:
        cs.execute(sql_one)
    except:
        conn.rollback()
    


def selectForUpdate(id, conn, cs):
    medcine = None
    sql = ("select id,brand_name,ingredient,dosage,wrapping,effects,before_using,dosing,"
            "precautions,possible,stora,picture,getid,jpid,lang,creat_by,creat_at,update_by,update_at"
            " from chim_mast"
            " where id = {0}").format(id)
    cs.execute(sql)
    if cs.rowcount > 0:
        dataRow = cs._rows[0]
        medcine = {
            'id': dataRow[0],
            'brand_name': dataRow[1],
            'ingredient': dataRow[2],
            'dosage': dataRow[3],
            'wrapping': dataRow[4],
            'effects': dataRow[5],
            'before_using': dataRow[6],
            'dosing': dataRow[7],
            'precautions': dataRow[8],
            'possible': dataRow[9],
            'stora': dataRow[10],
            'picture': dataRow[11],
            'getid': dataRow[12],
            'jpid': dataRow[13],
            'lang': dataRow[14],
            'creat_by': dataRow[15],
            'creat_at': dataRow[16],
            'update_by': dataRow[17],
            'update_at': dataRow[18],
        }
    return medcine

def insertMedcineToDB(medcine, conn, cs):
    medcine["creat_at"] = datetime.datetime.now()
    medcine["creat_by"] = PROG_ID
    medcine["update_at"] = datetime.datetime.now()
    medcine["update_by"] = PROG_ID
    add_sql = ("INSERT INTO chim_mast(id,brand_name,ingredient,dosage,wrapping,effects,before_using,dosing,"
                "precautions,possible,stora,picture,getid,jpid,lang,creat_by,creat_at,update_by,update_at)"
                " VALUES (%(id)s,%(brand_name)s,%(ingredient)s,%(dosage)s,%(wrapping)s,%(effects)s,%(before_using)s,%(dosing)s,"
                "%(precautions)s,%(possible)s,%(stora)s,%(picture)s,%(getid)s,%(jpid)s,%(lang)s,%(creat_by)s,%(creat_at)s,%(update_by)s,%(update_at)s)")
    cs.execute(add_sql,medcine)


def updateMedcineToDB(medcine, conn, cs):
    medcine["update_at"] = datetime.datetime.now()
    medcine["update_by"] = PROG_ID
    update_sql = (
        "UPDATE test.chim_mast              "
        "SET brand_name = %(brand_name)s,   "
        "  ingredient = %(ingredient)s,     "
        "  dosage = %(dosage)s,             "
        "  wrapping = %(wrapping)s,         "
        "  effects = %(effects)s,           "
        "  before_using = %(before_using)s, "
        "  dosing = %(dosing)s,             "
        "  precautions = %(precautions)s,   "
        "  possible = %(possible)s,         "
        "  stora = %(stora)s,               "
        "  picture = %(picture)s,           "
        "  getid = %(getid)s,               "
        "  jpid = %(jpid)s,                 "
        "  lang = %(lang)s,                 "
        "  update_by = %(update_by)s,       "
        "  update_at = %(update_at)s        "
        "WHERE id = %(id)s                  ")
    cs.execute(update_sql, medcine)

def saveMedcineToDB(medcine, conn , cs):
    try:
        oldMedcine = selectForUpdate(medcine['id'], conn, cs)
        if oldMedcine is None:
            insertMedcineToDB(medcine, conn, cs)
        else:
            updateMedcineToDB(medcine, conn, cs)
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False

def setGetMedcineStat(id, stat, retry, cs):
    cs.execute("UPDATE url_mast SET get_state = {0},retry = {1} WHERE id = {2}".format(stat,retry,id))

def setGetMedcineStatlock(id, stat, cs):
    cs.execute("UPDATE url_mast SET get_state = {0} WHERE id = {1}".format(stat,id))

def getOnePageToGet(conn, cs):
    urlMast_rec = None
    while(True):
        cs.execute("SELECT id,url,getid,jpid,lang,get_state,retry FROM url_mast WHERE id = (SELECT MIN(id) FROM url_mast t WHERE get_state = 0) FOR UPDATE")
        if (cs.rowcount == 0):
            break
        urlList = cs._rows[0]
        id =  urlList[0]
        getState = urlList[5]
        if (getState == 0):
            setGetMedcineStatlock(id, 1, cs)
            conn.commit()
            urlMast_rec = urlList
            break
        else:
            conn.rollback()
    return urlMast_rec


# sql_one ="select * from chim_mast"
# getUrl(sql_one)
