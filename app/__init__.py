from flask import Flask
from .config import DevConfig
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_bootstrap import Bootstrap
from .config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.sessin_protection = "strong"
login_manager.login_view = "auth.login"
photos = UploadSet('photos',IMAGES)
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    # Registering the blueprint
    from .main import main as main_blueprint
    from flask_uploads import UploadSet,configure_uploads,IMAGES
    app.register_blueprint(main_blueprint)
    #authentication
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    # setting config
    from .requests import configure_request
    from flask_uploads import configure_uploads
    configure_request(app)
    # configure UploadSet
    configure_uploads(app,photos)
    return app