from cerebralcortex.apiserver_v1 import CC
from cerebralcortex.apiserver_v1.core.decorators import auth_required
from cerebralcortex.kernel.DataStoreEngine.Data.minio_storage import MinioStorage
from cerebralcortex.apiserver_v1.core.data_models import auth_data_model
from flask import request
import json
import flask
from flask import send_file, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_raw_jwt, decode_token
from flask_restplus import Namespace, Resource
from datetime import datetime, timedelta


object_route = CC.configuration['routes']['object']
object_api = Namespace(object_route, description='Object(s) Data Storage')

@object_api.route('/')
class MinioObjects(Resource):
    #@auth_required
    #@object_api.header("Authorization", 'Bearer JWT', required=True)
    def get(self):
        '''List all available buckets'''
        bucket_list = MinioStorage(CC).list_buckets()
        return bucket_list, 200

@object_api.route('/<string:bucket_name>')
@object_api.doc(params={"bucket_name": "Name of the bucket in Minio storage."})
@object_api.response(404, 'The specified bucket does not exist or name is invalid.')
class MinioObjects(Resource):
    #@auth_required
    #@object_api.header("Authorization", 'Bearer JWT', required=True)
    def get(self, bucket_name): #TODO: bucketname cannot be less than 3 char
        '''List objects in a buckets'''
        objects_list = MinioStorage(CC).list_objects_in_bucket(bucket_name)
        if "error" in objects_list and objects_list["error"]!="":
            return objects_list["error"], 404

        print(objects_list)

        return objects_list, 200

@object_api.route('/stats/<string:bucket_name>/<string:object_name>')
@object_api.doc(params={"bucket_name": "Name of the bucket.", "object_name": "Name of the object."})
@object_api.response(404, 'The specified bucket/object does not exist or name is invalid.')
class MinioObjects(Resource):
    #@auth_required
    #@object_api.header("Authorization", 'Bearer JWT', required=True)
    def get(self, bucket_name, object_name): #TODO: bucketname cannot be less than 3 char
        '''Object properties'''
        objects_stats = MinioStorage(CC).get_object_stat(bucket_name, object_name)
        if "error" in objects_stats and objects_stats["error"]!="":
            return objects_stats["error"], 404
        return json.loads(objects_stats), 200

@object_api.route('/<string:bucket_name>/<string:object_name>')
@object_api.doc(params={"bucket_name": "Name of the bucket.", "object_name": "Name of the object."})
@object_api.response(404, 'The specified bucket does not exist or name is invalid.')
class MinioObjects12(Resource):
    #@auth_required
    #@object_api.header("Authorization", 'Bearer JWT', required=True)
    #@object_api.marshal_with(auth_data_model(object_api), envelope='resource')
    def get(self, bucket_name, object_name): #TODO: bucketname cannot be less than 3 char
        '''Download an object'''
        object = MinioStorage(CC).get_object(bucket_name, object_name)

        if "error" in object and object["error"]!="":
            return object["error"], 404

        return Response(object.data, mimetype=object.getheader("content-type"))