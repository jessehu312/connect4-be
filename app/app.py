import os
from flask import Flask, render_template
from . import settings, controllers, routes
from .socketio import init_socketio, blueprint
from flask_cors import CORS

project_dir = os.path.dirname(os.path.abspath(__file__))

def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='')
    cors = CORS(app)
    app.config.from_object(config_object)

    register_socketio(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_socketio(app):
    socketio = init_socketio(app)
    if __name__ == "__main__":
        socketio.run(app)

def register_blueprints(app):
    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(routes.api.blueprint)
    app.register_blueprint(blueprint)

def register_errorhandlers(app):
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

