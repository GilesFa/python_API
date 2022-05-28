import requests
import json
import os
import struct
import ctypes
from mod.changBG import changeBG_

#使用api取得cat的jpg下載網址
url = "https://api.thecatapi.com/v1/images/search"
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

#傳換成json格式
data = json.loads(response.text)
print(data)
#取出url的value
url = (data[0]['url'])
print("url=",url)

#取出url中的jpg名稱
url_sp = url.split('/')
jpgname = url_sp[4]

#將url路徑的jpg檔案下載並更換檔名成cat_開頭+原檔名.jpg
r = requests.get(url, allow_redirects=True)
open(f'C:\\github\\python_API\\demo1_cat\\img\\cat_{jpgname}', 'wb').write(r.content)

#建立jpg的新路徑
#JPGPATH = f'C:\\github\\python_API\\demo1_cat\\img\\cat_{jpgname}'
JPGPATH = f'C:\\github\\python_API\\demo1_cat\\img\\cat_RfpiTrLZ4.jpg'

#將jpg檔案路徑導入changGB模組進行更換windows桌面
changeBG_(JPGPATH)


# try:
#    os.rmdir(f'C:\\github\\python_API\\demo1_cat\\程式被運行') 
# except IOError:
#    print("FileExistsError: [WinError 183] 當檔案已存在時，無法建立該檔案")
# else:
#     os.mkdir(f'C:\\github\\python_API\\demo1_cat\\程式被運行')