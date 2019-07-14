from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # WTForms takes these as custom validators and
    # invokes them in addition to the stock validators

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LocationForm(FlaskForm):
    location = StringField("", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LocationListForm(FlaskForm):
    locations = RadioField(choices=None,
                           coerce=str,
                           validators=[DataRequired()])
    submit = SubmitField("Submit")


class RestaurantChoiceForm(FlaskForm):
    yes = SubmitField("I am eating here")
    no = SubmitField("Find me another restaurant")