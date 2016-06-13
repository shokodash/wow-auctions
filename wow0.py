
import pymysql
import time
import urllib.request
import json

def getFiles():
    requesturl = 'https://eu.api.battle.net/wow/auction/data/outland?locale=en_GB&apikey=vyaa7heguj4qysbpyxc4sbhacgera8n2'
    try:
        print('requesting url: ' + requesturl)
        with urllib.request.urlopen(requesturl) as reqopen:
            openread = reqopen.read()
            encoding = reqopen.info().get_content_charset('utf-8')
            print(openread)
            reqjson = json.loads(openread.decode(encoding))
            return reqjson
    except Exception as err:
        print(err)


def reqjson2db(reqjson, Connection):
    for i in reqjson['Files']:
        if isnew(Connection, i['lastModified']):
            datajson = url2json(i['url'])
            json2db(datajson, i['lastModified'], Connection)



def isnew(Connection, lastmod):
    try:
        with Connection.cursor() as curs:
            querystr = 'select * from meta0 where timejson=%s'
            query_return = curs.execute(querystr, lastmod)
            if query_return > 0:
                return False
            else:
                return True
    except Exception as err:
        print(err)
    return False

        
def url2json(dataurl):
    datajson = ''
    try:
        print('requesting url: ' + dataurl)
        with urllib.request.urlopen(dataurl) as dataopen:
            openread = dataopen.read()
            print(openread)
            encoding = dataopen.info().get_content_charset('utf-8')
            datajson = json.loads(openread.decode(encoding))
    except Exception as err:
        print(err)
    return datajson


def json2db(datajson, lastmodified, connection):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as curs:
            querystr = 'insert into meta (timeinsert, timejson) values (%s, %s)'
            curs.execute(querystr, (now, lastmodified))
            lastrowid = curs.lastrowid
        json2dbdata(Connection, datajson, lastrowid)
        connection.commit()
        print(lastrowid)
    except Exception as e1:
        print (e1)


def json2dbdata(connection, datajson, metaid):
    try:
        with connection.cursor() as cur:
            counter = 0
            for i in datajson['auctions']:
                counter = counter + 1
                if counter % 1000 == 0:
                    print(str(counter) + ' lines processed')
                querystr = 'insert into data (ownerrealm, itemid, bid, metaid) values (%s, %s, %s, %s)'
                cur.execute(querystr, (i['ownerRealm'], i['item'], i['bid'], metaid))
    except Exception as err:
        print(err)


while True:
    try:
        reqjsonfiles = getFiles()
        print('\n' + str(reqjsonfiles) + '\n')
        Connection = pymysql.connect(
            host='localhost', 
            user='root', 
            password='patsanpizdos', 
            db='wowauction',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        reqjson2db(reqjsonfiles, Connection)
        Connection.close()
    except Exception as e1:
        print (e1)
    print('Enter Sleep')
    time.sleep(300)
    print('Exit Sleep')
    




    
    
