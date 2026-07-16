from datetime import date, datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Todo
from ..forms import TodoForm
from ..ai_reminder import get_reminders, get_insights

todos_bp = Blueprint("todos", __name__)


@todos_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = Todo(
            task=form.task.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            due_time=form.due_time.data,
            user_id=current_user.id,
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("todos.index"))

    # ---- search & filtering ----
    filter_type = request.args.get("filter", "all")
    priority_filter = request.args.get("priority", "all")
    search_query = request.args.get("q", "").strip()

    query = Todo.query.filter_by(user_id=current_user.id)

    if filter_type == "completed":
        query = query.filter_by(completed=True)
    elif filter_type == "pending":
        query = query.filter_by(completed=False)

    if priority_filter in ("High", "Medium", "Low"):
        query = query.filter_by(priority=priority_filter)

    if search_query:
        query = query.filter(Todo.task.ilike(f"%{search_query}%"))

    todos = query.order_by(Todo.completed.asc(), Todo.due_date.asc().nullslast()).all()

    reminders = get_reminders(current_user)
    insights = get_insights(current_user)

    return render_template(
        "index.html",
        todos=todos,
        today=date.today(),
        form=form,
        filter_type=filter_type,
        priority_filter=priority_filter,
        search_query=search_query,
        reminders=reminders,
        insights=insights,
    )


@todos_bp.route("/complete/<int:id>", methods=["POST"])
@login_required
def complete(id):
    t = Todo.query.get_or_404(id)
    if t.user_id == current_user.id:
        t.completed = not t.completed
        t.completed_at = datetime.utcnow() if t.completed else None
        db.session.commit()
    return redirect(url_for("todos.index"))


@todos_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    t = Todo.query.get_or_404(id)
    if t.user_id == current_user.id:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for("todos.index"))


@todos_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        return redirect(url_for("todos.index"))

    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        todo.task = form.task.data
        todo.priority = form.priority.data
        todo.due_date = form.due_date.data
        todo.due_time = form.due_time.data
        db.session.commit()
        return redirect(url_for("todos.index"))

    return render_template("edit.html", form=form, todo=todo)
