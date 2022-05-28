from flask import Flask
from flask_restful import Api
# from resources.user import Users, User
from resources.user import Users
from resources.account import Accounts, Account

#將網站放到app變數中
app = Flask(__name__)
#將app轉換成api server
api = Api(app)
#建立api資源，指定從Users class物件尋找，且web路由為/users
api.add_resource(Users, '/users')
# api.add_resource(User, '/user/<id>')
# api.add_resource(Accounts, '/user/<user_id>/accounts')
# api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.route('/')
def index():
  return 'hello 123'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)