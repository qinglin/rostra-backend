from flask import Flask, make_response
from flask_mongoengine import MongoEngine
from flask_restx import Resource, Api, fields
from flask_cors import CORS
from models import Guild
from flask import jsonify
import uuid

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
            "result": guilds
        })


@rostra_conf.route('/guild/<guild_id>', methods=['GET'])
@rostra_conf.doc(params={'guild_id': 'guild id'})
@api.response(200, 'Query Successful')
@api.response(500, 'Internal Error')
class Get(Resource):
    def get(self, guild_id):
        try:
            query_by_guild_id = Guild.objects(guild_id=guild_id)
            print(query_by_guild_id)
            if query_by_guild_id is not None and len(query_by_guild_id) != 0:
                return jsonify({
                    "result": query_by_guild_id[0]
                })
            else:
                return {"result": ''}, 200
        except Exception as e:
            return {'error': str(e)}


@rostra_conf.route('/guild/get/<address>', methods=['GET'])
@rostra_conf.doc(params={'address': 'wallet address'})
@api.response(200, 'Query Successful')
@api.response(500, 'Internal Error')
class Get(Resource):
    def get(self, address):
        try:
            query_by_address = Guild.objects(creator=address)
            print(query_by_address)
            if query_by_address is not None and len(query_by_address) != 0:
                return jsonify({
                    "result": query_by_address
                })
            else:
                return {"result": []}, 200
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
    'name': fields.String(required=True, description='The guild name identifier'),
    "desc": fields.String,
    "creator": fields.String,
})


@rostra_conf.route('/guild/add/', methods=['POST'])
class Add(Resource):
    @rostra_conf.doc(body=resource_fields, responses={201: 'Guild Created'})
    @api.response(500, 'Internal Error')
    @api.response(401, 'Validation Error')
    def post(self):
            data = api.payload
            name = data['name']
            desc = data['desc']
            creator = data['creator']

            # validation if the guild name already exists
            if len(Guild.objects(name=name)) != 0:
                return {'message': 'The Guild Name Already Exists! Please change your guild name'}, 401

            guild = Guild(
                guild_id=str(uuid.uuid4()),
                name=name,
                desc=desc,
                creator=creator,
            )

            guild.save()
            return {'message': 'SUCCESS'}, 201

