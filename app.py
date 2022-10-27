from flask import Flask, render_template, session, redirect, url_for
from requests import request
from formulaires import Login
import functions

app = Flask(__name__)
app.config['SECRET_KEY'] = "MonSuperSecret" # Création de la clé de sécurité (Chiffrement des sessions et formulaires)

@app.route("/boutique/")
def afficher_boutique():
    articles_boutique = functions.shop_get_all_items()
    return render_template("boutique/boutique.html", articles = articles_boutique)

@app.route("/boutique/<id>", methods=['GET', 'POST'])
def boutique(id):
    article = functions.shop_get_item(int(id))

    return render_template("boutique/article.html", article = article)