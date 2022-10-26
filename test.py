from pymongo import MongoClient
import hashlib
from datetime import date, datetime

client = MongoClient("mongodb://localhost:27017")

db = client["RedFace"]

users = db.users
articles = db.articles
admins = db.admins

user = {
    "pseudo" : None,
    "prenom" : None,
    "nom" : None,
    "mail" : None,
    "password" : None,
    "age" : None,
    "date_register" : None
}

article = {
    "title" : None,
    "img" : None,
    "content" : None,
    "author" : None,
    "date_creation" : None,
    "commentary" : None
}

commentary = {
    "author" : None,
    "message" : None,
    "date" : None
}

## FONCTIONS

def get_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M")
    return date

def create_user(pseudo, prenom, nom, mail, password, age):
    password = hashlib.sha256(password.encode()).hexdigest()

    user = {
        "pseudo" : pseudo,
        "prenom" : prenom,
        "nom" : nom,
        "mail" : mail,
        "password" : password,
        "age" : age,
        "date_register" : get_date()
    }

    users.insert_one(user)

def delete_user(mail):
    users.delete_one(filter={
        "mail" : mail
    })

def create_article(title, img, content, author):
    date = get_date()
    article = {
        "title" : title,
        "img" : img,
        "content" : content,
        "author" : author,
        "date_creation" : date,
        "commentary" : [],
        "id" : str(hashlib.sha256((title+date).encode()).hexdigest())
    }

    articles.insert_one(article)

def create_commentary(articleid, author, message):
    commentary = {
        "author" : author,
        "message" : message,
        "date" : get_date(),
        "id" : None
    }

def get_article(id):
    article = articles.find_one({"id" : id})
    print(article)

def get_article_id(title, date):
    id = str(hashlib.sha256((title+date).encode()).hexdigest())
    return id

def create_admin(pseudo, prenom, nom, mail, password, age):
    password = hashlib.sha256(password.encode()).hexdigest()

    admin = {
        "pseudo" : pseudo,
        "prenom" : prenom,
        "nom" : nom,
        "mail" : mail,
        "password" : password,
        "age" : age,
        "date_register" : get_date()
    }

    admins.insert_one(admin)

#create_admin("Virtux", "Thomas", "Dlmp", "test@test.fr", "test", 22)
# create_user("Virtux", "Thomas", "Dlmp", "test@test.fr", "test123", 22)
# delete_user("test@test.fr")

#create_article("tet-st", "https://fghjkl.png", "lorem ipsum", "Moi")
#create_commentary("", "toto", "tata")


#get_article(get_article_id("tet-st", "19/10/2022 16:22"))