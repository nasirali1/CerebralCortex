from flask import request
from flask_restplus import Namespace, Resource

from cerebralcortex.apiserver_v1 import CC
from cerebralcortex.apiserver_v1.core.data_models import auth_data_model

object_route = CC.configuration['routes']['object']
object_api = Namespace(object_route, description='Object(s) Data Storage')

@object_api.route('/')
class data(Resource):
    #method_decorators = [jwt_required]
    @object_api.doc('Object Storage')
    #@stream_api.expect(auth_data_model(auth_api), validate=True)
    #@stream_api.marshal_list_with(auth_data_model(stream_api))
    def get(self):
        '''Post Data'''
        dp = request.json.get('dp', None)

        return dp, 200

@object_api.route('/<string:id>')
@object_api.doc(params={"id": "Object ID"})
class data(Resource):
    #method_decorators = [jwt_required]
    @object_api.doc('Object Storage')
    #@stream_api.expect(auth_data_model(auth_api), validate=True)
    #@stream_api.marshal_list_with(auth_data_model(stream_api))
    def get(self, id):
        '''Post Data'''
        print(id+" - dddd")
        #dp = request.json.get('dp', None)

        return 200