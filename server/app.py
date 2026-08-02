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

from resources.auth import Signup, Login, Logout, CheckSession
from resources.tasks import TaskList, TaskDetail

api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/me")

api.add_resource(TaskList, "/tasks")
api.add_resource(TaskDetail, "/tasks/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)