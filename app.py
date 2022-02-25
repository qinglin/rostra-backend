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


@rostra_conf.route('/guild/get/<ipfsAddr>', methods=['GET'])
@rostra_conf.doc(params={'ipfsAddr': 'ipfs addr'})
@api.response(200, 'Query Successful')
@api.response(500, 'Internal Error')
class Get(Resource):
    def get(self, ipfsAddr):
        try:
            query_by_ipfsAddr = Guild.objects(ipfsAddr=ipfsAddr)
            print(query_by_ipfsAddr)
            if query_by_ipfsAddr is not None and len(query_by_ipfsAddr) != 0:
                return jsonify({
                    "result": query_by_ipfsAddr
                })
            else:
                return {"result": []}, 200
        except Exception as e:
            return {'error': str(e)}




# nft = rostra_conf.model('Nft', {
#     'name': fields.String,
#     'baseURI': fields.String
# })


resource_fields = rostra_conf.model('guild', {
    'name': fields.String(required=True, description='The guild name identifier'),
    "desc": fields.String,
    "creator": fields.String,
    "ipfsAddr": fields.String(required=True, description='The ipfs address of the guild')
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
            ipfsAddr = data['ipfsAddr']

            # validation if the guild name already exists
            if len(Guild.objects(name=name)) != 0:
                return {'message': 'The Guild Name Already Exists! Please change your guild name'}, 401

            guild = Guild(
                guild_id=str(uuid.uuid4()),
                name=name,
                desc=desc,
                creator=creator,
                ipfsAddr=ipfsAddr
            )
            guild.save()
            return {'message': 'SUCCESS'}, 201


@rostra_conf.route('/guild/delete/<guild_id>', methods=['DELETE'])
@rostra_conf.doc(params={'guild_id': 'Id of the guild'})
class Delete(Resource):
    @api.response(201, 'Guild Deleted')
    @api.response(500, 'Internal Error')
    @api.response(401, 'Validation Error')
    def delete(self, guild_id):
        try:
            query_by_guild_id = Guild.objects(guild_id=guild_id)
            print(query_by_guild_id)

            if query_by_guild_id is not None and len(query_by_guild_id) != 0:
                query_by_guild_id.delete()
                return {'message': 'SUCCESS'}, 201
            else:
                return {"messgae": 'The Guild Id cannot be found'}, 401

        except Exception as e:
            return {'error': str(e)}

