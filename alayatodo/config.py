
class Config:
    DATABASE = '/tmp/alayatodo.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TODOS_PER_PAGE = 3
    TODOS_PER_PAGE_LIST = [1, 3, 6, 9, 12, 15]
    TODOS_DEFAULT_FILTER = 'all'
    DEBUG = True
    SECRET_KEY = 'd93a3aa0f654cd43048d418367189bc6'
    USERNAME = 'admin'
    PASSWORD = 'default'
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    TODOS_PER_PAGE = 5
