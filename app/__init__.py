from flask import Flask
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from config import Config


socketio = SocketIO()
bootstrap = Bootstrap()


def create_app(config_class=Config, debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(config_class)
    
    #app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    print(f"app\__init__.py:  Secret Key = {app.config['SECRET_KEY']}")

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    socketio.init_app(app)
    bootstrap.init_app(app)
    return app