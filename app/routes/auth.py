from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..models import User
from ..forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("todos.index"))

    form = LoginForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("todos.index"))
        error = "❌ Invalid username or password"

    return render_template("login.html", form=form, error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("todos.index"))

    form = RegisterForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data.strip()

        if User.query.filter_by(username=username).first():
            error = "❌ Username already exists"
        else:
            user = User(username=username)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("register.html", form=form, error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
