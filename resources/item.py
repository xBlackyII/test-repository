from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price: This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    """
    Da wir mit Resourcen arbeiten, benötigt die Api-App eine Resource,
    die durch eine Klasse dargestellt wird.
    """
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # Anstatt selbst zu suchen, kann ich die self.get()-Methode nutzen. Da diese
        # aber einen JWT-Token voraussetzt, wurde der Inhalt nach find_by_name ausgelagert
        # und diese als KLASSENMETHODE deklariert!!
        # #if next(filter(lambda x: x['name'] == name, items), None) is not None:
        if ItemModel.find_by_name(name):
            return {'message': 'An item with same "{}" already exists.'.format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # 500: internal server error.
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
