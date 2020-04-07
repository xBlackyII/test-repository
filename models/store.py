from db import db
from resources.item import ItemModel


class StoreModel(db.Model):
    """
    This class is an internal representation of the Item data.
    """
    # Tell the DB the tablename...
    __tablename__ = "stores"

    # ... and announcing the table entries.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # This is a back-reference to the store.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': list(map(lambda x: x.json(), self.items.all()))}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        """Saving the model to the database."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        """Find name in database.

        This function query by the given 'name' inside the database. Due to 
        'ItemModel' is query by a database model we can use the database functions
        like 'query'. Please note we can add more filter categories like:
        'ItemModel.query.filter_by(name=name).filter_by(id=id)

        :param cls: Class object.
        :type cls: Class object.
        :param name: The name to search for.
        :type name: str
        :returns: An item model.
        :rtype: ItemModel
        """
        return ItemModel.query.filter_by(name=name).first()
