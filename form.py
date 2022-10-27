from dataclasses import field
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class Login(FlaskForm):
    mail = StringField('Votre adresse mail : ', validators=[DataRequired()])
    password = PasswordField('Votre mot de passe : ', validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class Register(FlaskForm):
    nom = StringField('Votre nom : ', validators=[DataRequired()])
    prenom = StringField('Votre prenom : ', validators=[DataRequired()])
    mail = StringField('Votre adresse mail : ', validators=[DataRequired()])
    pseudo = StringField('Votre pseudonyme : ', validators=[DataRequired()])
    password = PasswordField('Votre mot de passe : ', validators=[DataRequired()])
    submit = SubmitField("S'inscrire")