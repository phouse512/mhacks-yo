from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['MONGODB_DB'] = 'mhacks'
app.config['MONGODB_HOST'] = 'ds031671.mongolab.com'
app.config['MONGODB_PORT'] = 31671
app.config['MONGODB_USERNAME'] = 'phil'
app.config['MONGODB_PASSWORD'] = 'house'

app.config["SECRET_KEY"] = "secretwords"

db = MongoEngine(app)
flask_bcrypt = Bcrypt(app)


def register_blueprints(app):
    # Prevents circular imports
    from core.views import core
    app.register_blueprint(core)

register_blueprints(app)

if __name__ == '__main__':
    app.run()