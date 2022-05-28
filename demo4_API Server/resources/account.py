from ast import Try
import re
from urllib import response
from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback #traceback.print_exc()函數使用

#限制用戶端可上傳的欄位資料
parser = reqparse.RequestParser()
parser.add_argument('account_name')
parser.add_argument('sex')
parser.add_argument('age')
parser.add_argument('user_id')


class Accounts(Resource):
    def db_init(self):
        #db連線設定
        db = pymysql.connect(host='127.0.0.1', user='root', password='umec@123', database='api')
        #當從db獲取資料時將其轉換成字典(Key與value的形式)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        sql = 'Select * From api.accounts Where deleted is not True and user_id = {}'.format(user_id)
        if arg['sex'] != None:
            sql += ' and sex = "{}"'.format(arg['sex'])
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        print(accounts)
        db.close
        return jsonify({"data": accounts}) 
              
    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        accounts={
            "account_name": arg['account_name'],
            "sex": arg['sex'],
            "age": arg['age'],
            "user_id": arg['user_id']
        }
        # print(accounts)
        query = []
        #將user輸入的key與value存入query list中
        for keys, values in accounts.items():
            if values != None:
                query.append(keys)
        query = ", ".join(query)
        #print(query)
        #INSERT INTO `api`.`accounts` (`account_name`, `sex`, `age`) VALUES ('TT', 'TT', '66');
        #將query的值帶入sql執行語句中
        sql = """
        INSERT INTO `api`.`accounts` ({}) VALUES ('{}', '{}', '{}', '{}');
        """.format(query ,accounts['account_name'], accounts['sex'], accounts['age'], accounts['user_id'])
        #print(sql)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = "新增成功"
        except:
            traceback.print_exc()
            response['msg'] = '新增失敗'

        db.commit()
        db.close
        return jsonify(response)

class Account(Resource):
    def db_init(self):
        #db連線設定
        db = pymysql.connect(host='127.0.0.1', user='root', password='umec@123', database='api')
        #當從db獲取資料時將其轉換成字典(Key與value的形式)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()

        #取得表格內存在且未被標示delete的所有id值
        sq1 = """
        Select * From api.accounts Where deleted is not True"""
        cursor.execute(sq1)
        db.commit()
        id_list = cursor.fetchall()
        id_box = []
        for item in id_list:
            #print(item['id'])
            id_box.append(item['id'])
        #判斷user輸入的id是否存在
        if int(id) in id_box:
            sq2 = """
            Select * From api.accounts Where deleted is not True and id = '{}'""".format(id)
            cursor.execute(sq2)
            db.commit()
            accounts = cursor.fetchone()
            db.close
            return jsonify({"data": accounts})
        else:
            return jsonify({"data": f"id:{id}，不存在"})
         

    def delete(self, user_id, id):
        db, cursor = self.db_init()
        #取得表格內存在且未被標示delete的所有id值
        sq1 = """
        Select * From api.accounts Where deleted is not True and user_id = {}""".format(user_id)
        cursor.execute(sq1)
        db.commit()
        id_list = cursor.fetchall()
        id_box = []
        for item in id_list:
            #print(item['id'])
            id_box.append(item['id'])
        #判斷user輸入的id是否存在
        if int(id) in id_box:
            sq2 = """
            UPDATE `api`.`accounts` SET deleted = True WHERE (`id` = {});""".format(id)
            response = {}
            try:
                cursor.execute(sq2)
                response["msg"] = "刪除成功"
            except:
                traceback.print_exc()
                response['msg'] = '刪除失敗'
            db.commit()
            db.close
            return jsonify(response)
        else:
            return jsonify({"data": f"id:{id}，不存在"})

    def patch(self, user_id, id):
        #獲取初始化的db與cursor
        db, cursor = self.db_init()
        #將user輸入的資料存放到arg變數中，且以字典的格式
        arg = parser.parse_args()
        print(arg)
        #確認id是否存在
        sql = 'Select * From api.accounts Where deleted is not True and user_id = {}'.format(user_id)
        cursor.execute(sql)
        db.commit()
        account_id = cursor.fetchall()
        #計算users table共有多少筆資料，並將存在的id值存入id_number list中
        id_count = 0
        id_number = []
        for item in account_id:
            id_count+=1
            id_number.append(item['id'])
        print(id_number)
        #判斷user輸入的id是否存在id_number list中，若有執行單筆資料更新
        if int(id) in id_number:
            query = []
            for key, value in arg.items():
                print(key,value)
                if value != None:
                    query.append(key + "=" + f"'{value}'")
            query = ", ".join(query)
            
            sq2 = """
            UPDATE `api`.`accounts` SET {} WHERE (`id` = '{}');
            """.format(query, id)
            print(sq2)
    
            response = {}
            try:
                #執行sql資料新增
                cursor.execute(sq2)
                response['msg'] = '資料修改成功'
            except:
                #於終端機列印出錯誤訊息
                traceback.print_exc()
                response['msg'] = '資料修改失敗'
            db.commit()
            db.close()
            return jsonify(response)
        else:
            return jsonify({'data': 'id不存在'})   
