from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.create_all()


from app.main import main as main_blueprint

app.register_blueprint(main_blueprint)

