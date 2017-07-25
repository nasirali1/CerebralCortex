from flask import request
from flask_restplus import Namespace, Resource
from cerebralcortex.apiserver_v1.core.decorators import auth_required

from cerebralcortex.apiserver_v1 import CC
from cerebralcortex.apiserver_v1.core.data_models import stream_data_model

stream_route = CC.configuration['routes']['stream']
stream_api = Namespace(stream_route, description='Data and annotation streams')

@stream_api.route('/')
class Stream(Resource):
    @auth_required
    @stream_api.doc('Post Stream Data')
    @stream_api.header("Authorization", 'Bearer JWT', required=True)
    @stream_api.expect(stream_data_model(stream_api), validate=True)
    @stream_api.marshal_list_with(stream_data_model(stream_api))
    def put(self):
        '''Put Stream Data'''

        raw_data = request.json.get('raw_data', None)

        return {"Posted Raw data": raw_data}, 200