from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_DB'] = 'mhacks'
app.config['MONGODB_HOST'] = 'ds031671.mongolab.com'
app.config['MONGODB_PORT'] = 31671
app.config['MONGODB_USERNAME'] = 'phil'
app.config['MONGODB_PASSWORD'] = 'house'

app.config["SECRET_KEY"] = "secretwords"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()