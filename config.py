import os

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = "OMG_DONT_READ"
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEBUG = True
	DEVELOPMENT = True

class DevelopmentConfig(Config):
	DEBUG = True
	DEVELOPMENT= True

class TestingConfig(Config):
	TESTING = True


