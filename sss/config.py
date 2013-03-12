# Defaults userful for testing
DATABASE = 'data.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % DATABASE

# Don't forget to turn debug mode off in production!
DEBUG = True

INTERFACE = '0.0.0.0'
PORT = 5000

BOOTSTRAP_FONTAWESOME = True
SECRET_KEY = 'wtfkey'
