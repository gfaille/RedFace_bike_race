from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Desert_race"]

users = db.Utilisateurs

blog = db.Blog

article_blog = blog.find()

#user_3 = users.find()

for elt in article_blog:
    print(elt)

#print(article_blog)

"""commentaire_utilisateur= {
    "Commentaire 3" : "Aurélien c'est le meilleur !"
}

blog.insert_one({"_id" : "ObjectId('634ff6940e65dc11426999fd')", "Commentaires" : commentaire_utilisateur})"""