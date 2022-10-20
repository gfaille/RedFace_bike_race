from datetime import date
import hashlib
from pymongo import MongoClient

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

#users.insert_one(dico_admin)
#blog.insert_one(dico_blog)
#forum.insert_one(dico_forum)

commentaire_utilisateur= {
    "Commentaire 4" : "Ce n'est qu'un au revoir Kévin"
}

def ajouter_commentaire_article(ID:int, commentaire:dict) -> None:

    a_modifier = blog.find_one({"ID" : ID})
    a_modifier["Commentaires"].append(commentaire)

    blog.update_one({"ID" : ID}, {"$set" : {"Commentaires" : a_modifier["Commentaires"]}})

def age(date_de_naissance:tuple) -> int:
    """Retourne l'âge de l'utilisateur
    :param date_de_naissance: Année, Mois, Jour
    """

    today = date.today()
    age = today.year - date_de_naissance[0] - ((today.month, today.day) < (date_de_naissance[1], date_de_naissance[2]))
    return age

date_de_naissance = (1991, 4, 3)

print(age(date_de_naissance))

"""def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

print(age(date(2000, 1, 1)))"""


jour = "1"
titre = "1er article"
id = hashlib.sha256((jour.encode()) + (titre.encode())).hexdigest()
print(id)
print(type(id))