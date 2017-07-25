from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from cerebralcortex.apiserver_v1.apis import blueprint
from cerebralcortex.apiserver_v1 import CC

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = CC.configuration['apiserver']['secret_key']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(CC.configuration['apiserver']['token_expire_time']))

jwt = JWTManager(app)
app.register_blueprint(blueprint)
app.secret_key = 'super-secret' # Change this!
app.run(debug=True, host=CC.configuration['apiserver']['host'], port=CC.configuration['apiserver']['port'])



