from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restx import Resource, Api, fields
import json

from models import Guild
from models import Nft
from models import Members

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'guild',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
api = Api(app, version='1.0', title='Rostra Backend API',
          description='Rostra Backend Restful API')
rostra_conf = api.namespace('Rostra', description='Rostra APIs')


@rostra_conf.route('/get-guilds/', methods=['GET'])
@api.response(200, 'Query Successful')
class Get(Resource):
    def get(self):
        guilds = Guild.objects()
        return {"result": guilds.to_json()}


@rostra_conf.route('/get-guilds/<address>', methods=['GET'])
@rostra_conf.doc(params={'address': 'wallet address'})
@api.response(200, 'Query Successful')
class Get(Resource):
    def get(self, address):
        print(address)
        query_by_address = Guild.objects(wallet_address=address)
        return {"result": query_by_address.to_json()}


nft = rostra_conf.model('Nft', {
    'name': fields.String,
    'baseURI': fields.String
})

members = rostra_conf.model('members', {
    'nfts': fields.List(fields.Nested(nft)),
    'guilds': fields.List(fields.Integer)
})

resource_fields = rostra_conf.model('guild', {
    "guild_id": fields.Integer(required=True, description='The guild id identifier'),
    'name': fields.String(required=True, description='The guild name identifier'),
    "desc": fields.String,
    "creator": fields.String,
    "wallet_address": fields.String(required=True, description='The user wallet address'),
    "signature": fields.String,
    "members": fields.Nested(members)
})


@rostra_conf.route('/add-guild/', methods=['POST'])
class Add(Resource):
    @rostra_conf.doc(body=resource_fields, responses={201: 'Guild Created'})
    @api.response(500, 'Internal Error')
    def post(self):
        try:
            data = api.payload
            guild_id = data['guild_id']
            name = data['name']
            desc = data['desc']
            creator = data['creator']
            wallet_address = data['wallet_address']
            signature = data['signature']
            nfts = data['members']['nfts']
            guilds = data['members']['guilds']
            guilds_array = []
            for guild in guilds:
                guilds_array.append(int(guild))
            print(guilds_array)
            nft_array = []
            for nft in nfts:
                nft_name = nft['name']
                nft_baseURI = nft['baseURI']
                nft_obj = Nft(name=nft_name, baseURI=nft_baseURI)
                nft_array.append(nft_obj)
            print(nft_array)
            members = Members(nfts=nft_array, guilds=guilds_array)
            guild = Guild(name=name,
                          guild_id=guild_id,
                          desc=desc,
                          creator=creator,
                          wallet_address=wallet_address,
                          signature=signature,
                          members=members)

            guild.save()
            return json.dumps({'message': 'SUCCESS'})
        except Exception as e:
            return json.dumps({'error': str(e)})

