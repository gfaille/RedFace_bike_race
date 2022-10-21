import hashlib
from datetime import date
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

#db.create_collection("Utilisateurs")
#db.create_collection("Blog")
#db.create_collection("Forum")

users = db.Utilisateurs
blog = db.Blog
forum = db.Forum

##################
#Utilisateurs
##################

def create_user(nom:str, prenom:str, date_de_naissance:str, age:int, sexe:str, telephone:str, adresse_mail:str) -> None:
    """Créer un utilisateur
    :param nom: Nom de famille de l'utilisateur
    :param prenom: Prénom de l'utilisateur
    :param date_de_naissance : Date de naissance de l'utilisateur
    :param age: Age de l'utilisateur
    :param sexe: Sexe de l'utilisateur
    :param telephone: Numéro de téléphone de l'utilisateur
    :param adresse_mail: Adresse e-mail de l'utilisateur
    """

    pass

def create_admin(nom:str, prenom:str, date_de_naissance:str, age:int, sexe:str, telephone:str, adresse_mail:str) -> None:
    """Créer un administrateur
    :param nom: Nom de famille de l'administrateur
    :param prenom: Prénom de l'administrateur
    :param date_de_naissance : Date de naissance de l'administrateur
    :param age: Age de l'administrateur
    :param sexe: Sexe de l'administrateur
    :param telephone: Numéro de téléphone de l'administrateur
    :param adresse_mail: Adresse e-mail de l'administrateur
    """

    pass

def delete_user(adresse_mail:str) -> None:
    """Supprime un utilisateur
    :param adresse_mail: Adresse mail de l'utilisateur a supprimer
    """

    pass

def calculate_age(date_de_naissance:tuple) -> int:
    """Retourne l'âge de l'utilisateur
    :param date_de_naissance: Année, Mois, Jour
    """

    pass

##################
#Blog - Articles
##################

def create_article(nom:str, prenom:str, titre:str, texte:str) -> None:
    """Créer un article de blog
    :param nom: Nom de l'utilisateur créant l'article
    :param prénom: Prénom de l'utilisateur créant l'article
    :param titre: Titre de l'article
    :param texte: Texte de l'article
    """

    auteur = nom + "." + prenom
    date_du_jour = date.today()
    maj = None
    ID = hashlib.sha256((str(date_du_jour).encode()) + (titre.encode())).hexdigest()

    blog.insert_one({"ID" : ID, "Auteur" : auteur, "Date" : str(date_du_jour), "Mise à jour" : maj, "Titre" : titre, "Texte" : texte, "Commentaires" : []})

def update_article(id:str, titre:str, texte:str) -> None:
    """Met à jour un article
    :param id: ID de l'article à mettre à jour
    :param titre: Nouveau titre de l'article à mettre à jour
    :param texte: Nouveau texte de l'article à mettre à jour
    """
    
    a_modifier = blog.find_one({"ID" : id})
    a_modifier["Titre"] = titre
    a_modifier["Texte"] = texte
    a_modifier["Mise à jour"] = str(date.today())

    blog.update_one({"ID" : id}, {"$set" : {"Titre" : a_modifier["Titre"], "Texte" : a_modifier["Texte"], "Mise à jour" : a_modifier["Mise à jour"]}})

def delete_article(id:str) -> None:
    """Supprime un article
    :param id: ID de l'article a supprimer
    """

    pass

##################
#Blog - Commentaires
##################

def add_comment():
    pass

def update_comment():
    pass

def delete_comment():
    pass