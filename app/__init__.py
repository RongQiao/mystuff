from flask import Flask
from app.routes.browser import browser_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(browser_bp)
    return app
