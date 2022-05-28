from flask import Flask
from flask_restful import Api
from resources.user import Users

app = Flask(__name__)
api =Api(app)


@app.route('/')
def index():
    return "index"

api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8881", debug=True)
