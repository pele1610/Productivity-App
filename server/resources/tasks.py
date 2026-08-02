from flask import request, session
from flask_restful import Resource

from models import db, Task, User


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


class TaskList(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized"}, 401

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = Task.query.filter_by(user_id=user.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        tasks = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed
            }
            for t in pagination.items
        ]

        return {
            "tasks": tasks,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200

    def post(self):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()

        try:
            new_task = Task(
                title=data.get("title"),
                description=data.get("description"),
                completed=data.get("completed", False),
                user_id=user.id
            )
            db.session.add(new_task)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

        return {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }, 201


class TaskDetail(Resource):
    def patch(self, id):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized"}, 401

        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404

        if task.user_id != user.id:
            return {"error": "Forbidden"}, 403

        data = request.get_json()

        try:
            if "title" in data:
                task.title = data["title"]
            if "description" in data:
                task.description = data["description"]
            if "completed" in data:
                task.completed = data["completed"]
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }, 200

    def delete(self, id):
        user = get_current_user()
        if not user:
            return {"error": "Unauthorized"}, 401

        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404

        if task.user_id != user.id:
            return {"error": "Forbidden"}, 403

        db.session.delete(task)
        db.session.commit()

        return {}, 204