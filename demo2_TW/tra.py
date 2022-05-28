from hashlib import sha1
import hmac
from this import s
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from matplotlib.backend_bases import LocationEvent
from requests import request
from pprint import pprint
import json
import math
import geocoder


app_id = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
app_key = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        # print("目前的時間:",xdate)

        #進行加密
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        # print(hashed)

        #加密後的字串
        signature = base64.b64encode(hashed.digest()).decode()
        # print(signature)

        #授權資料
        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        #print(authorization)

        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/Station?%24format=JSON', headers= a.get_auth_header())
    data = json.loads(response.text)
    #pprint(data)
    
    #1.範例
    # my_lat = 25.035441
    # my_lon = 121.499922

    #2.自己的位置
    location = geocoder.ip('me').latlng
    print(location)
    my_lat = location[0]
    my_lon = location[1]

    #3.變數初始值
    min_result = 9999

    for station in data['Stations']:
        lat = station['StationPosition']['PositionLat']
        lon = station['StationPosition']['PositionLon']
        result = math.sqrt((my_lat-lat) * (my_lat-lat) + (my_lon-lon) * (my_lon-lon))
        if min_result > result:
            min_result = result
            result_name = station['StationName']['Zh_tw']
        # pprint(result)
        # pprint(station['StationName'])
    print(f"離目前經度{my_lat},緯度{my_lon}最近的車站為:",result_name)