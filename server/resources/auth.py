from flask import request, session
from flask_restful import Resource

from models import db, User


class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "Username already taken"}, 400

        try:
            new_user = User(username=username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

        session["user_id"] = new_user.id

        return {"id": new_user.id, "username": new_user.username}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id
            return {"id": user.id, "username": user.username}, 200

        return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        session.clear()
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.get(user_id)
            if user:
                return {"id": user.id, "username": user.username}, 200

        return {"error": "Not logged in"}, 401