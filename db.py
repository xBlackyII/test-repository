from flask_sqlalchemy import SQLAlchemy

# Here we create a link to the models with the objective to map the objects
# directly into the DB.
# To do this it is necessary to inheritance the Models from db.Model!
db = SQLAlchemy()
