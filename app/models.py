from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    theme = db.Column(db.String(10), default="light", nullable=False)  # "light" or "dark"

    todos = db.relationship(
        "Todo", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), default="Medium")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    due_time = db.Column(db.Time)  # optional — powers the "due in 15 minutes" AI reminder
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)  # powers streaks / "you complete tasks in the evening"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
