#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, User, Task

fake = Faker()

with app.app_context():

    print("Clearing existing data...")
    Task.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating users...")
    users = []
    for _ in range(3):
        user = User(username=fake.unique.user_name())
        user.password_hash = "password123"
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating tasks...")
    tasks = []
    for user in users:
        for _ in range(4):
            task = Task(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=2),
                completed=fake.boolean(),
                user_id=user.id
            )
            tasks.append(task)

    db.session.add_all(tasks)
    db.session.commit()

    print(f"Done! Created {len(users)} users and {len(tasks)} tasks.")