from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

#db.create_collection("Utilisateurs")
#db.create_collection("Blog")
#db.create_collection("Forum")

users = db.Utilisateurs
blog = db.Blog

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

#users.insert_one(dico_admin)

#blog.insert_one(dico_blog)

"""user_3 = users.find()

for elt in user_3:
    print(elt)"""

#print(user_3)

commentaire_utilisateur= {
    "Commentaire 4" : "Ce n'est qu'un au revoir Kévin"
}

def ajouter_commentaire_article(ID:int, commentaire:dict) -> None:

    a_modifier = blog.find_one({"ID" : ID})
    a_modifier["Commentaires"].append(commentaire)

    blog.update_one({"ID" : ID}, {"$set" : {"Commentaires" : a_modifier["Commentaires"]}})