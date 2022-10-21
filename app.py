from pymongo import 
from datetime import datetime
client = MongoClient("mongodb://localhost:27017/")
db = client["app"]


###################
### Utilisateur ###
###################

# Créer la base de donnée "User" sur mongodb

db.create_collection("User")

# Ajouter un utilisateur à la base de donnée "User"

db.User.insert_one({
    "Nom" : input ("Votre nom"),
    "Prénom" : input ("Votre prénom"),
    "Pseudo" : input ("Choisir un pseudo"),
    "Mot_de_passe" : ("Choisir un mot de passe"),
    "Email" : ("Entrez votre mail")
})

# Sélectionner le mot de passe et le pseudo dans la base de donnée "User" pour pouvoir vérifier à la connection si les informations sont entrer sont correcte

db.User.find({"Mot_de_passe"}, {"Pseudo"})


################
### Articles ###
################

# Créer la base de donnée "Articles"

db.create_collection("Articles")

# Ajouter un article à la base de donnée "Articles"

db.Articles.insert_one({
    "Pseudo" : db.User.inser({"Pseudo"}),
    "Date": datetime.today().strftime('%Y-%m-%d'),
    "Titre": input("Titre de votre article"),
    "Article": input ("Veuillez tapez votre article ici"),
})

# Supprimer un article




####################
### Commentaires ###
####################

# Créer de la base de donnée "Commentaires"

db.create_collection("Commentaires")

# Ajouter un commentaire à la base de donnée "Commentaires"

db.Commentaires.inser_one({
    "Pseudo" : db.User.inser({"Pseudo"}),
    "Date": datetime.today().strftime('%Y-%m-%d'),
    "Commentaire" : input("Veuillez taper votre commentaire ici")
})