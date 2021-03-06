
import pymysql
import time
import urllib.request
import json


def url2json(url):
    return_json = ''
    try:
        print('requesting url: ' + url)
        with urllib.request.urlopen(url) as openobj:
            openread = openobj.read()
            encoding = openobj.info().get_content_charset('utf-8')
            return_json = json.loads(openread.decode(encoding))
    except Exception as err:
        print('url2json: ' + str(err))
    return return_json

def reqjson2db(reqjson, Connection):
    for i in reqjson['files']:
        if isnew(Connection, i['lastModified']):
            datajson = url2json(i['url'])
            json2db(datajson, i['lastModified'], Connection)

def isnew(Connection, lastmod):
    try:
        with Connection.cursor() as curs:
            querystr = 'select * from meta where timejson=%s'
            query_return = curs.execute(querystr, lastmod)
            if query_return > 0:
                print('Not New')
                return False
            else:
                print('New')
                return True
    except Exception as err:
        print('isnew: ' + str(err))
    return False

def json2db(datajson, lastmodified, connection):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as curs:
            querystr = 'insert into meta (timeinsert, timejson) values (%s, %s)'
            curs.execute(querystr, (now, lastmodified))
            lastrowid = curs.lastrowid
        json2dbdata(Connection, datajson, lastrowid)
        connection.commit()
        print('lastrowid: ' + str(lastrowid))
    except Exception as err:
        print ('json2db: ' + str(err))

def json2dbdata(connection, datajson, metaid):
    try:
        with connection.cursor() as cur:
            counter = 0
            for i in datajson['auctions']:
                counter = counter + 1
                if counter % 1000 == 0:
                    print(str(counter) + ' lines processed')
                querystr = 'insert into data (auc, item, owner, ownerrealm, bid, buyout, quantity, timeleft, rand, seed, context, metaid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(querystr, (i['auc'], i['item'], i['owner'], i['ownerRealm'], i['bid'], i['buyout'], i['quantity'], i['timeLeft'], i['rand'], i['seed'], i['context'], metaid))
    except Exception as err:
        print('json2dbdata: ' + str(err))

reqjsonurl = 'https://eu.api.battle.net/wow/auction/data/outland?locale=en_GB&apikey=vyaa7heguj4qysbpyxc4sbhacgera8n2'
while True:
    try:
        reqjson = url2json(reqjsonurl)
        Connection = pymysql.connect(
            host='localhost', 
            user='testuser', 
            password='ThreeFour34$', 
            db='wowauction',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        print('Connected to MySQL server')
        reqjson2db(reqjson, Connection)
        Connection.close()
    except Exception as err:
        print ('Main Body: ' + str(err))
    print('Enter Sleep')
    time.sleep(300)
    print('Exit Sleep')
    




    
    
