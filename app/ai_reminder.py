"""
Lightweight, rule-based "AI" reminder & insights engine.

No external AI/LLM API calls are made here on purpose — everything is
derived from patterns already in the user's own task data (due times,
completion timestamps, priorities). That keeps this feature instant,
free to run, and safe to deploy without any extra API keys.
"""
from collections import Counter
from datetime import date, datetime, timedelta

from .models import Todo


def get_reminders(user):
    """Time-sensitive banners shown at the top of the dashboard."""
    reminders = []
    now = datetime.now()
    todos = Todo.query.filter_by(user_id=user.id, completed=False).all()

    # Tasks with a specific due date + time that are due very soon
    for t in todos:
        if t.due_date and t.due_time:
            due_dt = datetime.combine(t.due_date, t.due_time)
            minutes_left = (due_dt - now).total_seconds() / 60
            if 0 <= minutes_left <= 15:
                reminders.append({
                    "type": "warning",
                    "icon": "🤖",
                    "title": "AI Reminder",
                    "message": (
                        f'"{t.task}" is due in {max(int(minutes_left), 0)} minute(s). '
                        "Complete it before it becomes overdue."
                    ),
                })
            elif 15 < minutes_left <= 60:
                reminders.append({
                    "type": "info",
                    "icon": "🤖",
                    "title": "AI Reminder",
                    "message": f'"{t.task}" is due in {int(minutes_left)} minutes.',
                })

    # Overdue tasks (date-only tasks count as overdue once the day has passed;
    # timed tasks count as overdue once their due time has passed today)
    overdue_count = 0
    for t in todos:
        if not t.due_date:
            continue
        if t.due_date < date.today():
            overdue_count += 1
        elif t.due_date == date.today() and t.due_time and datetime.combine(t.due_date, t.due_time) < now:
            overdue_count += 1

    if overdue_count > 0:
        reminders.append({
            "type": "danger",
            "icon": "⚠️",
            "title": "AI Reminder",
            "message": f"You have {overdue_count} overdue task{'s' if overdue_count != 1 else ''}.",
        })

    return reminders


def get_insights(user):
    """Friendly, data-driven insight strings shown on the dashboard."""
    all_todos = Todo.query.filter_by(user_id=user.id).all()
    if not all_todos:
        return ["👋 Add your first task to start getting personalized insights!"]

    completed = [t for t in all_todos if t.completed]
    pending = [t for t in all_todos if not t.completed]
    insights = []

    # Overall completion rate
    rate = round(len(completed) / len(all_todos) * 100)
    insights.append(f"📊 {rate}% of your tasks are completed.")

    # Total completed
    if completed:
        insights.append(
            f"🎯 You have completed {len(completed)} task{'s' if len(completed) != 1 else ''} overall."
        )

    # Completed this week
    week_ago = datetime.now() - timedelta(days=7)
    completed_this_week = [t for t in completed if t.completed_at and t.completed_at >= week_ago]
    if completed_this_week:
        insights.append(f"📈 You completed {len(completed_this_week)} task(s) this week.")

    # Most productive time of day
    hours = [t.completed_at.hour for t in completed if t.completed_at]
    if len(hours) >= 3:
        bucket = Counter()
        for h in hours:
            if 5 <= h < 12:
                bucket["morning"] += 1
            elif 12 <= h < 17:
                bucket["afternoon"] += 1
            elif 17 <= h < 22:
                bucket["evening"] += 1
            else:
                bucket["night"] += 1
        top_time = bucket.most_common(1)[0][0]
        insights.append(f"🧠 You usually complete tasks in the {top_time}.")

    # Completion streak
    streak = _completion_streak(completed)
    if streak >= 2:
        insights.append(f"🔥 You are on a {streak}-day completion streak!")

    # Tomorrow's workload
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_count = len([t for t in pending if t.due_date == tomorrow])
    if tomorrow_count >= 3:
        insights.append(f"📅 Tomorrow has {tomorrow_count} tasks. Consider finishing some today.")

    # Nudge toward the highest-priority open task
    high_priority_pending = [t for t in pending if t.priority == "High"]
    if high_priority_pending:
        insights.append(f'⭐ Finish "{high_priority_pending[0].task}" (High priority) first.')

    # Nothing due today
    today_count = len([t for t in pending if t.due_date == date.today()])
    if pending and today_count == 0:
        insights.append("😴 No tasks due today. Enjoy your day!")
    elif not pending:
        insights.append("😴 No pending tasks. Enjoy your day!")

    return insights


def _completion_streak(completed_todos):
    """Consecutive days (including today) with at least one completed task."""
    days = sorted({t.completed_at.date() for t in completed_todos if t.completed_at}, reverse=True)
    if not days:
        return 0

    streak = 0
    expected = date.today()
    for d in days:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == expected + timedelta(days=1):
            # duplicate date already counted, skip
            continue
        else:
            break
    return streak
