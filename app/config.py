from instance.config import MOVIE_API_KEY
import os
class Config:
    """
    General configuration class
    """
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    MOVIE_API_BASE_URL = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://patrick:flower2@localhost/watchlist'
    #  email configurations
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 587
   # MAIL_USE_TLS = True
   # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
   # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
class ProdConfig(Config):
    """
    Production configuration child class
    Args:
    Config: The parent configuration class with general configuration settings
    """
    pass
class DevConfig(Config):
    """
    Development configuration child class
    Args:
    config: 
    The parent configuration class with general configuration settings

    """
    DEBUG=True



config_options = {
    'development':DevConfig,
    'production':ProdConfig
    }   