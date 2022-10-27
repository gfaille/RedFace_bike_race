import hashlib
from datetime import date, datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

#db.create_collection("Boutique")

boutique = db.Boutique

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