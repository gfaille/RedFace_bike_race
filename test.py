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



"""nb_documents = forum.count_documents({})
print(nb_documents)
print(type(nb_documents))"""

"""crud.create_article("Dulompont", "Thomas", "Mon 1er article", "On débute")
id_article = blog.find_one({"Titre" : "Mon 1er article"})
print(id_article["ID"])
crud.update_article(id_article["ID"], "Mon 1er article", "On fais mieux")"""

#crud.add_comment_article("4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f","Dulompont", "Thomas", "C'est beau")

crud.delete_comment_article("4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f", "b7f740fa1ca6f862a1625e1ecc04ce385c941fd9594988f1576f36932fcd60fa")