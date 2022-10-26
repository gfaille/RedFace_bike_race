from dataclasses import field
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class Login(FlaskForm):
    mail = StringField('Votre adresse mail : ', validators=[DataRequired()], id="floatingInput")
    password = StringField('Votre mot de passe : ', validators=[DataRequired()], id="passwordInput")
    submit = SubmitField('Connexion')