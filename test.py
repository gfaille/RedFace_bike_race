import hashlib
from datetime import date, datetime
from pymongo import MongoClient

import functions

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

#function.add_comment_article("4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f","Dulompont", "Thomas", "C'est beau")

#function.delete_comment_article("4f6591887e147295b566ad97c812b2da9769174ebc4b5aa8e1a57a3ab459795f", "b7f740fa1ca6f862a1625e1ecc04ce385c941fd9594988f1576f36932fcd60fa")

#function.create_article("Alex", "Alex", "3eme article", "Bonjour")

"""article = function.get_article()

for article in article:
    print(article["Titre"], article["Texte"])"""

"""{% for article in articles %}

{% if article["ARCHIVE"] == 0 %}
{{article["NAME"], article["PRICE"], article["DESCRIPTION"]}}

{% elif article["ARCHIVE"] == 1 %}


{% endif %}

{% endfor %}"""

#function.shop_update_item(2, "Lit", "2000 €", "Un très beau lit")

functions.shop_add_new_field(2, "IMG", "lit.jpg")