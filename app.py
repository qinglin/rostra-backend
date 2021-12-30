from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restx import Resource, Api

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'guild',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
api = Api(app, version='1.0', title='Sample API',
          description='A sample API')


@api.route('/get-guilds/<address>', methods=['GET'])
@api.doc(params={'address': 'wallet address'})
class get(Resource):
    def get(self):
        return {'get': 'guild'}

