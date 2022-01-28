from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import json
from models import Guild
from models import Nft
from models import Requirements
from flask import jsonify, request


app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'guild',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
api = Api(app, version='1.0', title='Rostra Backend API',
          description='Rostra Backend Restful API')
rostra_conf = api.namespace('rostra', description='Rostra APIs')


@rostra_conf.route('/guild/get/', methods=['GET'])
@api.response(200, 'Query Successful')
@api.response(500, 'Internal Error')
class Get(Resource):
    def get(self):
        guilds = Guild.objects()
        return jsonify({
            "guilds": guilds
        })


@rostra_conf.route('/guild/get/<address>', methods=['GET'])
@rostra_conf.doc(params={'address': 'wallet address'})
@api.response(200, 'Query Successful')
@api.response(500, 'Internal Error')
class Get(Resource):
    def get(self, address):
        try:
            query_by_address = Guild.objects(members__in=[address])
            print(query_by_address)
            if query_by_address is not None and len(query_by_address) != 0:
                return {
                    "result": json.dumps(query_by_address)
                }, 200
            else:
                return {"result": {}}, 200
        except Exception as e:
            return {'error': str(e)}


member_fields = rostra_conf.model('member', {
    "guild_id": fields.Integer(required=True, description='The guild id identifier'),
    'wallet_address': fields.String(required=True, description='The wallet address of member'),
})


@rostra_conf.route('/guild/members/add/', methods=['POST'])
class Add(Resource):
    @rostra_conf.doc(body=member_fields, responses={201: 'Member added to Guild'})
    @api.response(500, 'Internal Error')
    def post(self):
        data = api.payload
        guild_id = data['guild_id']
        wallet_address = data['wallet_address']
        query_by_guild_id = Guild.objects(guild_id=guild_id)
        guild = query_by_guild_id[0]
        guild.members.append(wallet_address)
        guild.save()
        return {'message': 'SUCCESS'}, 201


nft = rostra_conf.model('Nft', {
    'name': fields.String,
    'baseURI': fields.String
})

members = rostra_conf.model('Requirements', {
    'nfts': fields.List(fields.Nested(nft)),
    'guilds': fields.List(fields.Integer)
})

resource_fields = rostra_conf.model('guild', {
    #"guild_id": fields.Integer(required=True, description='The guild id identifier'),
    'name': fields.String(required=True, description='The guild name identifier'),
    "desc": fields.String,
    "creator": fields.String,
    "members": fields.List(fields.String),
    "signature": fields.String,
    "requirements": fields.Nested(members)
})


@rostra_conf.route('/guild/add/', methods=['POST'])
class Add(Resource):
    @rostra_conf.doc(body=resource_fields, responses={201: 'Guild Created'})
    @api.response(500, 'Internal Error')
    def post(self):
       # try:
            data = api.payload
            print(api.payload)
            name = data['name']
            desc = data['desc']
            creator = data['creator']
            # wallet_address = data['wallet_address']
            signature = data['signature']
            nfts = data['requirements']['nfts']
            guilds = data['requirements']['guilds']
            guilds_array = []
            for guild in guilds:
                guilds_array.append(int(guild))
            nft_array = []

            for nft in nfts:
                nft_name = nft['name']
                nft_baseURI = nft['baseURI']
                nft_obj = Nft(name=nft_name, baseURI=nft_baseURI)
                nft_array.append(nft_obj)
            requirements = Requirements(nfts=nft_array, guilds=guilds_array)
            guild = Guild(name=name,
                          desc=desc,
                          creator=creator,
                          #wallet_address=wallet_address,
                          signature=signature,
                          requirements=requirements)

            guild.save()
            return {'message': 'SUCCESS'}, 201
        #except Exception as e:
       #     return json.dumps({'error': str(e)})

