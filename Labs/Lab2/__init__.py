from module_1.views import mod as controllers
from flask import Flask

module_1 = Flask(__name__)
module_1.config.from_object('config')
module_1.register_blueprint(controllers)