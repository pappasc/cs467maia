from flask import Flask
from users import users_api
from users_signature import users_sig_api
from admins import admins_api
from awards import awards_api
from tests import tests_api
import os
 
# Create Flask application and use apis defined in other files
app = Flask(__name__)
app.register_blueprint(users_api)
app.register_blueprint(users_sig_api)
app.register_blueprint(admins_api)
app.register_blueprint(awards_api)
app.register_blueprint(tests_api)

