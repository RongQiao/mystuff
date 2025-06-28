from flask import Flask
from app.routes.browser import browser_bp


app = Flask(__name__)


def create_app():    
    app.register_blueprint(browser_bp)
    return app

@app.template_filter('thousands')
def thousands_filter(value):
    try:
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value
