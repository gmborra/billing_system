import os
import sys

from flask import Flask
from simple_settings import settings

from configuration.routes import api_bp

app_ = Flask(__name__)

def create_app():
    sys.path.append(os.path.join(settings.PROJECT_BASE_PATH).replace('\\', '//'))
    app_.config["DEBUG"] = settings.DEBUG
    app_.config["TESTING"] = settings.TESTING
    app_.config['ENV'] = settings.ENVIRONMENT

    app_.register_blueprint(api_bp)
    return app_