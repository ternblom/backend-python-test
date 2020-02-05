
class Config:
    DATABASE = '/tmp/alayatodo.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    DEBUG = True
    SECRET_KEY = 'd93a3aa0f654cd43048d418367189bc6'
    USERNAME = 'admin'
    PASSWORD = 'default'
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
