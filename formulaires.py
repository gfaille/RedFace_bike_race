from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email

class Login(FlaskForm):
    email = EmailField("Entrez votre email : ", validators=[DataRequired()])
    mdp = PasswordField("Entrez votre mot de passe :", validators=[DataRequired()])