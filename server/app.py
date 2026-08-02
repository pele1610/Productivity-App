from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from models import db, bcrypt
import config

app = Flask(__name__)
app.config.from_object(config)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
api = Api(app)

# Resources registered here

if __name__ == "__main__":
    app.run(port=5555, debug=True)