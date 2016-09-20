from flask import Flask

portal = Flask(__name__)
portal.secret_key = 'test'
from portal import views
