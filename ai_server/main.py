from flask import Flask

app = Flask(__name__)

from response.risk_response import risk_blueprint
#from response.significant_response import significant_blueprint

app.register_blueprint(risk_blueprint)
#app.register_blueprint(significant_blueprint)
