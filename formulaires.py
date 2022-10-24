from inspect import classify_class_attrs
from flask_wtf import FlaskForm
import wtforms as wtf

class Formlogin(FlaskForm):
    email = wtf.EmailField("Entrez votre adresse mail : ")
    mdp = wtf.PasswordField("Entrez votre mdp : ")
