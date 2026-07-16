from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Todo
from ..forms import ChangePasswordForm

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ChangePasswordForm()
    success = None
    error = None

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            error = "❌ Current password is incorrect"
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            success = "✅ Password updated successfully"
            form = ChangePasswordForm(formdata=None)  # clear the form

    todos = Todo.query.filter_by(user_id=current_user.id).all()
    completed = [t for t in todos if t.completed]
    stats = {
        "total": len(todos),
        "completed": len(completed),
        "pending": len(todos) - len(completed),
        "completion_rate": round(len(completed) / len(todos) * 100) if todos else 0,
    }

    return render_template("profile.html", form=form, stats=stats, error=error, success=success)


@profile_bp.route("/toggle-theme", methods=["POST"])
@login_required
def toggle_theme():
    current_user.theme = "dark" if current_user.theme == "light" else "light"
    db.session.commit()
    return jsonify({"theme": current_user.theme})
