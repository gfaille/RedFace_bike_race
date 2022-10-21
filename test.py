import hashlib
from datetime import date, datetime
from pymongo import MongoClient

import crud

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

#db.create_collection("Utilisateurs")
#db.create_collection("Blog")
#db.create_collection("Forum")

users = db.Utilisateurs
blog = db.Blog
forum = db.Forum

dico_admin =  {
    "Utilisateur 1" : "Anthony",
    "Utilisateur 2" : "Aurélien",
    "Utilisateur 3" : "Loïc",
    "Utilisateur 4" : "Thomas",
    "Utilisateur 5" : "Alexandre"
}

dico_blog = {
    "ID" : "001",
    "Titre" : "Article 4",
    "Auteur" : "Test",
    "Commentaires" : [
        {"Commentaire 1" : "C'est un bon article"},
        {"Commentaire 2" : "Très intéressant"}
    ]
}

dico_forum = {
    "Post" : "Post"
}

commentaire_utilisateur= {
    "Commentaire 4" : "Ce n'est qu'un au revoir Kévin"
}

def age(date_de_naissance:tuple) -> int:
    """Retourne l'âge de l'utilisateur
    :param date_de_naissance: Année, Mois, Jour
    """

    today = date.today()
    age = today.year - date_de_naissance[0] - ((today.month, today.day) < (date_de_naissance[1], date_de_naissance[2]))
    return age

"""date_de_naissance = (1991, 4, 3)

print(age(date_de_naissance))"""

"""def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

print(age(date(2000, 1, 1)))"""

"""nb_documents = forum.count_documents({})
print(nb_documents)
print(type(nb_documents))"""

"""crud.create_article("Dulompont", "Thomas", "Mon 1er article", "On débute")
id_article = blog.find_one({"Titre" : "Mon 1er article"})
print(id_article["ID"])
crud.update_article(id_article["ID"], "Mon 1er article", "On fais mieux")"""


def ajouter_commentaire_article(ID:str, nom:str, prenom:str, commentaire:str) -> None:

    nom = "dulompont"
    prenom = "Thomas"
    auteur = prenom + "." + nom.upper()[0]
    heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    a_modifier = blog.find_one({"ID" : ID})
    id_commentaire = hashlib.sha256((str(heure).encode()) + (auteur.encode())).hexdigest()

    dicommentaire = {
        "ID Commentaire" : id_commentaire,
        "Auteur" : auteur,
        "Date" : heure,
        "Commentaire" : commentaire
    }

    a_modifier["Commentaires"].append(dicommentaire)

    blog.update_one({"ID" : ID}, {"$set" : {"Commentaires" : a_modifier["Commentaires"]}})


#ajouter_commentaire_article("4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f", "Dulompont", "Thomas", "C'est moins")

"""a_modifier = blog.find_one({"ID" : "4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f"})
print(len(a_modifier["Commentaires"]))
nb = 0

for key in a_modifier:
    nb += 1

print(nb)"""

heure = "2022-10-21 16:42:31"
auteur = "Thomas.D"
id_commentaire = hashlib.sha256((str(heure).encode()) + (auteur.encode())).hexdigest()
print(id_commentaire)