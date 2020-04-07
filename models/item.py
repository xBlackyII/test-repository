from db import db


class ItemModel(db.Model):
    """This class is an internal representation of the Item data."""
    # Tell the DB the tablename...
    __tablename__ = "items"

    # ... and announcing the table entries.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Hier findet eine Verknüpfung zum Store statt. Dieses ItemModel wird
    # somit einen Store zugeordnet! Quasi: Du gehörst zu folgendem Store.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

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
