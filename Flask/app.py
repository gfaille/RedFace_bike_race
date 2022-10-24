from flask import Flask, render_template, session, redirect, url_for
from formulaires import Login
import function

app = Flask(__name__)
app.config['SECRET_KEY'] = "MonSuperSecret" # Création de la clé de sécurité (Chiffrement des sessions et formulaires)

@app.route("/")
def accueil():
    # Vérification des données contenues dans le cookie de session
    if "mail" in session and "mdp" in session:
        # Si une session contient bien un email et un mdp alors j'affiche hello world
        return "hello world"
    # Sinon je redirige vers la page de login
    return(redirect(url_for("login")))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = Login() # Je cree une instance de la classe Login (qui crée et gère le formulaire de login)
    #Vérification de : 1°) Je suis en POST, 2°) toutes les données demandées sont présentes
    if form.validate_on_submit():
        mail = form.data["email"]
        mdp = form.data["mdp"]
        # Création du cookie de session
        session["mail"] = mail
        session["mdp"] = mdp
        liste = [i for i in range(5)]
        return render_template("login_succes.html", login=mail, mdp=mdp, liste=liste)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    # Suppression du cookie de session
    session.clear()
    return redirect(url_for("login"))

@app.route("/postblog/")
def afficher_article():
    articles = function.get_all_article()
    return render_template("postblog.html", articles = articles)