from email import parser
from urllib import response
from flask_restful import Resource,reqparse
from flask import jsonify
import pymysql
import traceback
from urllib import response

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')


class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host="127.0.0.1", database="api_test", user="root", password="umec@123")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
        
    def get(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        sql = """select * from api_test.users where deleted is not True"""
        if arg['name'] != None:
            sql += ' and name ="{}" '.format(arg['name'])
        cursor.execute(sql)
        users = cursor.fetchall()
        db.commit()
        db.close()
        return jsonify({'data':users})

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0, 
            'birth': arg['birth'] or '1990-01-01',
            'note': arg['note'] or 'note',
        }
        sql = """INSERT INTO `api_test`.`users` (`name`,`gender`,`birth`,`note`) VALUES('{}','{}','{}','{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])
       
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = "ok"
        except:
            traceback.print_exc()
            response['msg'] = "ohoh"

        db.commit()
        db.close()

        return jsonify(response)
        