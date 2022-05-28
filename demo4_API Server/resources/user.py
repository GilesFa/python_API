from ast import Try
# import re
from urllib import response
from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback #traceback.print_exc()函數使用

#限制用戶端可上傳的欄位資料
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

# class User(Resource): #指定此class為api的資源，進行單筆資料操作
#     #資料庫初始化設定
#     def db_init(self):
#         #db連線設定
#         db = pymysql.connect(host='127.0.0.1', user='root', password='umec@123', database='api')
#         #當從db獲取資料時將其轉換成字典(Key與value的形式)
#         cursor = db.cursor(pymysql.cursors.DictCursor)
#         return db, cursor
    
#     def get(self, id): #當使用http get的方法時觸發以下程式
#         #獲取初始化的db與cursor
#         db, cursor = self.db_init()

#         #確認id是否存在
#         sql = 'Select * From api_test.users Where deleted is not True'
#         cursor.execute(sql)
#         db.commit()
#         users_id = cursor.fetchall()

#         #計算users table共有多少筆資料，並將存在的id值存入id_number list中
#         id_count = 0
#         id_number = []
#         for item in users_id:
#             id_count+=1
#             id_number.append(item['id'])
#             #列出talbe中所有id值
#             #print(item['id'])
#         print(f"總共有{id_count}筆資料")
#         #判斷user輸入的id是否存在id_number list中
#         if int(id) in id_number:
#             print(f"{id}存在{id_number}裡面")
#             #判斷id存在，進行以下quer動作:
#             #設定sql語法，篩選api子資料庫中的users table中的所有資料
#             sq2 = """Select * From api_test.users where id = '{}' """.format(id)
#             #由cursor執行sql語法
#             cursor.execute(sq2)
#             db.commit()
#             #取得cursor執行sql語法後所取得的所有資料
#             user = cursor.fetchone()
#             db.close()
#             #讓網頁可以json的形式顯示資料
#             return jsonify({'data': user})
#         else:
#             print(f"{id}不存在存在{id_number}裡面")
#             return jsonify({'data': 'id不存在'})        

#     def patch(self, id): #進行單筆資料更新
#         #獲取初始化的db與cursor
#         db, cursor = self.db_init()
#         #將user輸入的資料存放到arg變數中，且以字典的格式
#         arg = parser.parse_args()
#         #print(arg)

#         #確認id是否存在
#         sql = 'Select * From api_test.users Where deleted is not True'
#         cursor.execute(sql)
#         db.commit()
#         users_id = cursor.fetchall()
#         #計算users table共有多少筆資料，並將存在的id值存入id_number list中
#         id_count = 0
#         id_number = []
#         for item in users_id:
#             id_count+=1
#             id_number.append(item['id'])
#         #判斷user輸入的id是否存在id_number list中，若有執行單筆資料更新
#         if int(id) in id_number:
#             #將arg內的value與db中的user表格欄位名稱做對應
#             user = {
#                 'name': arg['name'],
#                 'gender': arg['gender'],
#                 'birth': arg['birth'],
#                 'note': arg['note'],       
#             }
#             query = []
#             for key, value in user.items():
#             #print(key,value)
#                 if value != None:
#                     query.append(key + "=" + f"'{value}'")
#             query = ", ".join(query)
#             sq2 = """
#             UPDATE `api_test`.`users` SET {} WHERE (`id` = '{}');
#             """.format(query, id)

#             response = {}
#             try:
#                 #執行sql資料新增
#                 cursor.execute(sq2)
#                 response['msg'] = '資料修改成功'
#             except:
#                 #於終端機列印出錯誤訊息
#                 traceback.print_exc()
#                 response['msg'] = '資料修改失敗'
        
#             db.commit()
#             db.close()
#             return jsonify(response)
#         else:
#             return jsonify({'data': 'id不存在'})   

#     def delete(self, id): #當使用http delete的方法時觸發以下程式
#         #獲取初始化的db與cursor
#         db, cursor = self.db_init()

#         #確認id是否存在
#         sql = 'Select * From api_test.users Where deleted is not True'
#         cursor.execute(sql)
#         db.commit()
#         users_id = cursor.fetchall()

#         #計算users table共有多少筆資料，並將存在的id值存入id_number list中
#         id_count = 0
#         id_number = []
#         for item in users_id:
#             id_count+=1
#             id_number.append(item['id'])

#         #判斷user輸入的id是否存在id_number list中
#         if int(id) in id_number:
#             print(f"{id}存在{id_number}裡面")
#             #判斷id存在，進行以下quer動作:
#             #設定sql語法，將特定id的欄位中的deleted值設定為True，用來代表軟刪除(布林值,TINYINT(1))，資料不會從db刪除，僅用來標示並用來讓其他sql語句引用
#             sq2 = """UPDATE `api_test`.`users` SET deleted = True WHERE (`id` = {}); """.format(id)
#             response = {}
#             try:
#                 #由cursor執行sql語法
#                 cursor.execute(sq2)
#                 response['msg'] = '資料刪除成功'
#             except:
#                 #於終端機列印出錯誤訊息
#                 traceback.print_exc()
#                 response['msg'] = '資料刪除失敗'
#             db.commit()
#             db.close()
#             return jsonify(response)
#         else:
#             print(f"{id}不存在存在{id_number}裡面")
#             return jsonify({'data': 'id不存在'})    

class Users(Resource): #指定此class為api的資源，進行多筆資料操作
    #資料庫初始化設定
    def db_init(self):
        #db連線設定
        db = pymysql.connect(host='127.0.0.1', user='root', password='umec@123', database='api')
        #當從db獲取資料時將其轉換成字典(Key與value的形式)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self): #當使用http get的方法時觸發以下程式
        #獲取初始化的db與cursor
        db, cursor = self.db_init()
        #取得使用者輸入的參數
        arg = parser.parse_args()
        #設定sql語法，篩選api子資料庫中的users table中的所有資料
        sql = 'Select * From api_test.users Where deleted is not True'
        #設定網址搜尋器: http://192.168.0.2:5000/users?gender=1，只列出gender為1的資料
        if arg['gender'] != None:
            sql += ' and gender = "{}"'.format(arg['gender'])
        if arg['name'] != None:
            sql += ' and name = "{}"'.format(arg['name'])
        print(sql)        
        #由cursor執行sql語法
        cursor.execute(sql)
        db.commit()
        #取得cursor執行sql語法後所取得的所有資料
        users = cursor.fetchall()
        db.close()
        print(users)
        #讓網頁可以json的形式顯示資料
        return jsonify({'data': users})

    def post(self): #當使用http post的方法時觸發以下程式
        #獲取初始化的db與cursor
        db, cursor = self.db_init()
        #將user輸入的資料存放到arg變數中，且以字典的格式
        arg = parser.parse_args()
        #將arg內的value與db中的user表格欄位名稱做對應
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '2000-01-01',
            'note': arg['note'] or 'xxx',        
        }
        #設定insert的語句，{}代表預設不填任何資料，並設置對應的變數欄位
        sql = """ 
        INSERT INTO `api_test`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])

        response = {}
        try:
            #執行sql資料新增
            cursor.execute(sql)
            response['msg'] = '資料新增成功'
        except:
            #於終端機列印出錯誤訊息
            traceback.print_exc()
            response['msg'] = '資料新增失敗'
    
        db.commit()
        db.close()
        return jsonify(response)