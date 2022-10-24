import hashlib
from datetime import date, datetime
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

def create_user(nom:str, prenom:str, pseudo:str, date_de_naissance:tuple, sexe:str, telephone:str, adresse_mail:str) -> None:
    """Créer un utilisateur
    :param nom: Nom de famille de l'utilisateur
    :param prenom: Prénom de l'utilisateur
    :param date_de_naissance : Date de naissance de l'utilisateur (Année - Mois - Jour)
    :param sexe: Sexe de l'utilisateur
    :param telephone: Numéro de téléphone de l'utilisateur
    :param adresse_mail: Adresse e-mail de l'utilisateur
    """
    role = 1
    date_inscription = date.today()
    age = calculate_age(date_de_naissance)
    
    users.insert_one({
        "Role": role , 
        "Nom": nom , "Prenom": prenom , 
        "Pseudo": pseudo,
        "Date_de_naissance": str(date_de_naissance), 
        "Age": age , 
        "Sexe": sexe , 
        "Telephone": telephone , 
        "Adresse_mail": adresse_mail , 
        "Date_inscription": str(date_inscription)})
    

def create_admin(nom:str, prenom:str, pseudo:str, date_de_naissance:str, age:int, sexe:str, telephone:str, adresse_mail:str) -> None:
    """Créer un administrateur
    :param nom: Nom de famille de l'administrateur
    :param prenom: Prénom de l'administrateur
    :param date_de_naissance : Date de naissance de l'administrateur
    :param age: Age de l'administrateur
    :param sexe: Sexe de l'administrateur
    :param telephone: Numéro de téléphone de l'administrateur
    :param adresse_mail: Adresse e-mail de l'administrateur
    """
    role = 0
    date_inscription = date.today()
    age = calculate_age(date_de_naissance)
    
    users.insert_one({
        "Role": role , 
        "Nom": nom , 
        "Prenom": prenom , 
        "Pseudo": pseudo,
        "Date_de_naissance": str(date_de_naissance), 
        "Age": age , 
        "Sexe": sexe , 
        "Telephone": telephone , 
        "Adresse_mail": adresse_mail , 
        "Date_inscription": str(date_inscription)})


def delete_user(pseudo:str) -> None:
    """Supprime un utilisateur
    :param adresse_mail: Adresse mail de l'utilisateur a supprimer
    """
    users.delete_one({"Pseudo": pseudo})


def calculate_age(date_de_naissance:tuple) -> int:
    """Retourne l'âge de l'utilisateur
    :param date_de_naissance: Année, Mois, Jour
    """
    today = date.today()
    age = today.year - date_de_naissance[0] - ((today.month, today.day) < (date_de_naissance[1], date_de_naissance[2]))
    return age

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

    blog.delete_one({"ID" : id})

def get_all_article() -> dict:
    """Renvoi tout les articles"""
    return blog.find()

##################
#Blog - Commentaires
##################

def add_comment_article(ID:str, nom:str, prenom:str, commentaire:str) -> None:
    """Ajoute un commentaire à l'article souhaité
    :param ID: ID de l'article sur lequel on souhaite ajouté le commentaire
    :param nom: Nom de l'utilisateur qui souhaite ajouter un commentaire
    :param prenom: Prénom de l'utilisateur qui souhaite ajouter un commentaire
    :param commentaire: Commentaire de l'utilisateur
    """

    auteur = prenom + "." + nom.upper()[0]
    heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id_commentaire = hashlib.sha256((str(heure).encode()) + (auteur.encode())).hexdigest()

    dicommentaire = {
        "ID Commentaire" : id_commentaire,
        "Auteur" : auteur,
        "Date" : heure,
        "Commentaire" : commentaire
    }
    
    a_modifier = blog.find_one({"ID" : ID})
    a_modifier["Commentaires"].append(dicommentaire)

    blog.update_one({"ID" : ID}, {"$set" : {"Commentaires" : a_modifier["Commentaires"]}})

def update_comment_article():
    pass

def delete_comment_article(id_article:str, id_commentaire:str) -> None:
    """Supprime un commentaire d'un article
    :param id_article: ID de l'article sur lequel supprimer le commentaire
    :param id_commentaire: ID du commentaire a supprimer
    """

    blog.update_one(
        {'ID': id_article},
        {'$pull': {"Commentaires":{ "ID Commentaire": id_commentaire}}}
        )