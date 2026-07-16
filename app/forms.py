from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Optional

USERNAME_PATTERN = r"^[A-Za-z0-9_]{4,}$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(USERNAME_PATTERN, message="Min 4 chars. Letters, numbers, _ only"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                PASSWORD_PATTERN,
                message="Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char (@$!%*?&)",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords don't match")],
    )
    submit = SubmitField("Register")


class TodoForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired(), Length(max=200)])
    priority = SelectField(
        "Priority", choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
    )
    due_date = DateField("Due Date", validators=[Optional()])
    due_time = TimeField("Due Time", validators=[Optional()])
    submit = SubmitField("Save")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Regexp(PASSWORD_PATTERN, message="Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char"),
        ],
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords don't match")],
    )
    submit = SubmitField("Update Password")
