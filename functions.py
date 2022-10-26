import hashlib
from datetime import date, datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

#db.create_collection("Utilisateurs")
#db.create_collection("Blog")
#db.create_collection("Forum")
#db.create_collection("Boutique")

users = db.Utilisateurs
blog = db.Blog
forum = db.Forum
boutique = db.Boutique

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

##################
#Boutique
##################

def shop_create_item(nom:str, prix:str, description:str) -> None:
    """Créer un article dans la boutique
    :param nom: Nom de l'article
    :param prix: Prix de l'article
    :param description : Description de l'article
    """

    date_ajout = date.today()
    archive = 0
    maj = None
    ID = boutique.count_documents({}) + 1

    boutique.insert_one({"ID" : ID, "NAME" : nom, "PRICE" : prix, "DESCRIPTION" : description, "DATE" : str(date_ajout), "MAJ" : maj, "ARCHIVE" : archive})

def shop_update_item(id:int, nom:str, prix:str, description:str) -> None:
    """Met à jour un article dans la boutique
    :param id: ID de l'article à mettre à jour
    :param nom: Nouveau titre de l'article à mettre à jour
    :param prix: Nouveau texte de l'article à mettre à jour
    :param description: Nouvelle description de l'article
    """
    
    a_modifier = boutique.find_one({"ID" : id})
    a_modifier["NAME"] = nom
    a_modifier["PRICE"] = prix
    a_modifier["DESCRIPTION"] = description
    a_modifier["MAJ"] = str(date.today())

    boutique.update_one({"ID" : id}, {"$set" : {"NAME" : a_modifier["NAME"], "PRICE" : a_modifier["PRICE"], "DESCRIPTION" : a_modifier["DESCRIPTION"], "MAJ" : a_modifier["MAJ"]}})

def shop_delete_item(id:int) -> None:
    """Archive un article de la boutique
    :param id: ID de l'article à archiver
    """

    a_modifier = boutique.find_one({"ID" : id})
    a_modifier["ARCHIVE"] = 1

    boutique.update_one({"ID" : id}, {"$set" : {"ARCHIVE" : a_modifier["ARCHIVE"]}})

def shop_get_item(id:int) -> dict:
    """Récupère un article de la boutique grâce à son ID
    :param id: ID de l'article à récupérer
    """

    return boutique.find_one({"ID" : id})

def shop_get_all_items() -> list:
    """Récupère tout les articles de la boutique"""

    articles = boutique.find()
    liste_articles = []

    for article in articles:
        liste_articles.append(article)

    return liste_articles

def shop_verify_item(id:int) -> bool:
    """Vérifie si un article existe déjà dans la boutique, renvoi True s'il existe, False s'il n'existe pas"""

    if boutique.count_documents({"ID" : id}):
        return True
    
    else:
        return False

def shop_add_new_field(id:int, cle:str, valeur:str) -> None:
    """Ajouter un nouveau champ dans un document
    :param id: ID du document où l'on souhaite ajouter un nouveau champ
    :param cle: Nom de la nouvelle clé
    :param valeur: Valeur de la nouvelle clé
    """

    boutique.update_one({"ID" : id}, {"$set" : {cle : valeur}})

def shop_cart(id) -> None:
    boutique.insert_one({"ID" : id})