import os

class Config(object):
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    # export APP_SETTINGS="config.DevelopmentConfig"
    # export DATABASE_URL='postgresql://USERNAME:PASSWORD@localhost/DBNAME'
    DEBUG = True
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = 'dfgsdfgseryrty456456ertu'
    # URI используемая для подключения к базе данных
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://test:test@localhost/todolist'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = False