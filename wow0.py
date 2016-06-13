
import pymysql
import time


def getFiles():
    import urllib.request
    import json
    requesturl = 'https://eu.api.battle.net/wow/auction/data/outland?locale=en_GB&apikey=vyaa7heguj4qysbpyxc4sbhacgera8n2'
    try:
        print('requesting url: ' + requesturl)
        with urllib.request.urlopen(requesturl) as urlopen_return:
            print(urlopen_return)
            data = urlopen_return.read()
            encoding = urlopen_return.info().get_content_charset('utf-8')
            print(data)
            jsonobject = json.loads(data.decode(encoding))
            return jsonobject['files']

    except Exception as err:
        print(err)


def array2db(filesarray, connection):
    for i in filesarray:
        if isnew(connection, i['lastModified']):
            jsondata = url2json(i['url'])
            json2db(jsondata, i['lastModified'], connection)

        
def url2json(url):
    import urllib.request
    import json
    jsonobject = ''
    try:
        print('requesting url: ' + url)
        with urllib.request.urlopen(url) as urlopen_return:
            data = urlopen_return.read()
            encoding = urlopen_return.info().get_content_charset('utf-8')
            jsonobject = json.loads(data.decode(encoding))
    except Exception as err:
        print(err)
    return jsonobject


def json2db(jsondata, lastmodified, connection):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cur:
            querystr = 'insert into meta0 (timeinsert, timejson) values (%s, %s)'
            cur.execute(querystr, (now, lastmodified))
            lastrowid = cur.lastrowid
        persistjsondata(Connection, jsondata, lastrowid)
        connection.commit()
        print(lastrowid)
    except Exception as e1:
        print (e1)


def persistjsondata(connection, jsondata, meta0id):
    try:
        with connection.cursor() as cur:
            counter = 0
            for i in jsondata['auctions']:
                counter = counter + 1
                if counter % 1000 == 0:
                    print('processed ' + str(counter) + ' lines')
                querystr = 'insert into data0 (ownerrealm, itemid, bid, meta0id) values (%s, %s, %s, %s)'
                cur.execute(querystr, (i['ownerRealm'], i['item'], i['bid'], meta0id))
                
    except Exception as err:
        print(err)


def isnew(connection, lastmod):
    try:
        with connection.cursor() as curr:
            querystr = 'select * from meta0 where timejson=%s'
            query_return = curr.execute(querystr, lastmod)
            if query_return > 0:
                return False
            else:
                return True
    except Exception as err:
        print(err)
    return False

while True:
    try:
        filesarray = getFiles()
        print('\n\n' + str(filesarray) + '\n')
        Connection = pymysql.connect(host='localhost', user='root', password='patsanpizdos', 
                     db='wowauction',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor )
        array2db(filesarray, Connection)
        Connection.close()
    except Exception as e1:
        print (e1)
    print('Enter Sleep')
    time.sleep(300)
    print('Exit Sleep')
    




    
    
