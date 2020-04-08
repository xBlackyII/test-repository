import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegistration
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)

app.config['DEBUG'] = True

# Erzeugt 'data.db' im Wurzelverzeichnis des Projekts.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'

# Anstatt die API "von Hand" zu definieren, wie in den vorherigen Beispielen,
# wird hier die "Api" von Flask_RESTful genutzt.
api = Api(app)


jwt = JWT(app, authenticate, identity)  # new endpoint /auth


# http://127.0.0.1:5000/item/<name>
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegistration, '/register')

if __name__ == "__main__":
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000, debug=True)
