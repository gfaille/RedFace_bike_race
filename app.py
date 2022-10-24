from flask import Flask, render_template, session, redirect, url_for
import formulaires

app = Flask(__name__)
app.config["SECRET_KEY"] = "MaCléfSecrèteTrèsSecrète"

@app.route("/") # création page web
def hello_world(): # création de la fonction accueil
    email = None
    if "email" in session: # vérification email dans le cookie
        email = session["email"]
    
    mdp = None
    if "mdp" in session: # vérification mdp dans le cookie
        mdp = session["mdp"]
    return render_template("index.html", email = email, mdp = mdp)


@app.route("/login/",methods = ["GET", "POST"]) # création page web
def test(): # création de la fonction connexion
    form = formulaires.Formlogin()
    if form.validate_on_submit():
        email = form.data["email"]
        mdp = form.data["mdp"]
        session["email"] = email
        session["mdp"] = mdp 
        return redirect(url_for("hello_world")) #rediriger vers la page d'accueil
    return render_template("login.html", form = form)

@app.route("/deco/") # création page web
def deco(): # création de la fonction déconnexion
    session.clear()
    return redirect(url_for("hello_world")) # rediriger vers la page d'accueil