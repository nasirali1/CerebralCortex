from flask import Blueprint
from flask_restplus import Api

from cerebralcortex.apiserver_v1.apis.auth import auth_api
from cerebralcortex.apiserver_v1.apis.stream import stream_api
from cerebralcortex.apiserver_v1.apis.object import object_api

blueprint = Blueprint('v1', __name__, url_prefix="/api/v1")
api_doc = '/docs/'

api = Api(blueprint,
          title='Cerebral Cortex',
          version='1.0',
          description='API server for Cerebral Cortex',
          contact='dev@md2k.org',
          license='BSD 2-Clause',
          license_url='https://opensource.org/licenses/BSD-2-Clause',
          doc=api_doc,
          )
api.add_namespace(auth_api)
api.add_namespace(stream_api)
api.add_namespace(object_api)
