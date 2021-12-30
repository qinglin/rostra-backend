from flask import Flask
from flask import request
from flask_mongoengine import MongoEngine
from flask_restplus import Api

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'guild',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
api = Api(app)


@api.route('/get-guilds/<id>', methods=['GET'])
@api.doc(params={'id': 'An ID'})
def get():
    print("get build")

