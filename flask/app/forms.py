from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')

class IPLPostMatchReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SelectPostType(FlaskForm):
    template = SelectField('Select Template',
        choices=[('01','IPL Post Match Review'), ('02', 'IPL Match Preview'), ('03', 'Generic Post'), ('04', 'Pod Cast')])
    submit = SubmitField('Submit')

