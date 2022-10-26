from pymongo import MongoClient
import hashlib
from datetime import date, datetime

client = MongoClient("mongodb://localhost:27017")

db = client["RedFace"]

users = db.users
blog = db.blog
admins = db.admins
forums_categories = db.forums_categories
forums_topics = db.forums_topics

def get_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M")
    return date

def create_id(author, date):
    id = str(hashlib.sha256((author+date).encode()).hexdigest())
    return id[0:10]

def create_user(is_admin, nom, prenom, mail, pseudo, password):

    hash_password = hashlib.sha256(password.encode()).hexdigest()

    date = get_date()
    if is_admin:
        role = 1
    else:
        role = 0
    user = {
        "id" : create_id(mail, date),
        "role" : role,
        "nom" : nom,
        "prenom" : prenom,
        "mail" : mail,
        "pseudo" : pseudo,
        "password" : hash_password
    }

    users.insert_one(user)

def verify_user(user_mail, user_password):
    """
    Fonction qui vérifie si l'adresse mail et le mot de passe entrés sont corrects
    : param user_mail (str) : Adresse mail de l'user
    : param user_password (str) : Mot de passe de l'user
    : return (bool) : Retourne True si il existe False sinon
    """

    # hash du mot de passe
    user_password = hashlib.sha256(user_password.encode()).hexdigest()

    infos_user = {
        "mail" : user_mail,
        "password" : user_password
        }

    is_register = users.find_one(infos_user)

    if is_register != None:
        return True
    else:
        return False

def get_info_user(mail):
    """
    Fonction qui renvoie les informations d'un user en fonction de l'email entré
    : user_mail (str) : Mail de l'user
    : return (dic) : Infos user
    """

    infos = users.find_one({"mail" : mail})

    if infos != None:
        return infos
    else:
        return {}

def get_all_user():
    """
    Fonction qui retourne la liste de tous les utilisateurs inscrits
    : return (list) : Liste des utilisateurs
    """

    all_user = users.find()
    list_users = []
    for user in all_user:
        list_users.append(user)
    return list_users

def get_all_postblog():
    """
    Fonction qui retourne la liste de tous les post de blog
    : return (list) : Liste des post
    """

    all_postblog = blog.find()
    list_postblogs = []
    for postblog in all_postblog:
        list_postblogs.append(postblog)
    return list_postblogs

def create_postblog(title, img, content, author):
    """
    Fonction qui créé un postblog dans la BDD
    : param title (str) : Titre du Post
    : param img (str) : URL de l'image
    : param content (str) : Contenu du Post
    : param author : Auteur du Post
    """
    date = get_date()
    id = create_id(author, date)
    postblog = {
        "title" : title,
        "img" : img,
        "content" : content,
        "author" : author,
        "date_creation" : date,
        "commentary" : [],
        "id" : id
    }

    blog.insert_one(postblog)

def modify_postblog(id, title, img, content):
    """
    Fonction qui modifie un postblog dans la BDD
    : param id (str) : id du post
    : param title (str) : Titre du Post
    : param img (str) : URL de l'image
    : param content (str) : Contenu du Post
    """
    date = get_date()

    post = blog.find_one({"id" : id})

    post["title"] = title
    post["img"] = img
    post["content"] = content

    blog.update_one({"id" : id}, {"$set": { "title" : post["title"], "img" : post["img"], "content" : post["content"]}});

def get_postblog(id):
    post = blog.find_one({"id" : id})
    return post

def create_commentary_postblog(id, commentary, author):
    """
    Fonction qui créée et ajoute un commentaire sur un Post
    : param id (str) : ID du Post
    : param commentary (str) : Le commentaire
    : param author (str) : L'auteur du commentaire
    """
    post = get_postblog(id)
    date = get_date()

    id_commentary = create_id(author, date)
    struc_commentary = {
        "id" : id_commentary[0:10],
        "auteur" : author,
        "date" : date,
        "commentaire" : commentary
        }

    post["commentary"].append(struc_commentary)

    blog.update_one({"id" : id}, {"$set": {"commentary" : post["commentary"]}});

def create_categorie_forum(name, author):
    """
    Fonction qui créée une catégorie pour le Forum
    : param name (str) : Nom de la catégorie
    """
    date = get_date()
    categorie = {
        "id" : create_id(author, date),
        "name" : name,
        "author": author,
        "date_creation" : date,
    }
    forums_categories.insert_one(categorie)

def delete_categorie_forum(id):
    """
    Fonction qui supprime une catégorie du Forum
    : param id (str) : ID de la catégorie
    """
    forums_categories.delete_one({"id" : id})

def get_categorie_forum(id):
    """
    Fonction qui retourne les informations d'une catégorie
    : param id (str) : ID de la categorie
    : return (dict) : La catégorie
    """
    categorie = forums_categories.find_one({"id" : id})
    return categorie

def create_topic_forum(title, content, author, categorie):
    """
    Fonction qui créée un topic de forum
    : param title (str) : Titre du topic
    : param content (str) : Contenu du topic
    : param author (str) : Auteur du topic
    : return (dict) : Infos du topic
    """
    date = get_date()

    topic = {
        "id" : create_id(author, date),
        "title" : str(title),
        "content" : str(content),
        "categorie": str(categorie),
        "date_creation" : str(date),
        "commentary" : [],
        "author" : str(author)
    }
    forums_topics.insert_one(topic)

def delete_topic_forum(id):
    """
    Fonction qui supprime un topic du Forum
    : param id (str) : ID du topic
    """
    forums_topics.delete_one({"id" : id})

def get_topic_forum(id):
    """
    Fonction qui retourne les informations du topic
    : param id (str) : ID du topic
    : return (dict) : La catégorie
    """
    topic = forums_topics.find_one({"id" : id})
    return topic

def get_all_categories_forum():
    """
    Fonction qui retourne la liste de toutes les catégories
    : return (list) : Liste des catégories
    """

    all_categories = forums_categories.find()
    list_categories = []
    for postblog in all_categories:
        list_categories.append(postblog)
    return list_categories

def get_all_topic_forum():
    """
    Fonction qui retourne la liste de tous les topic du forum
    : return (list) : Liste des topic
    """

    all_topics = forums_topics.find()
    list_topics = []
    for topic in all_topics:
        list_topics.append(topic)
    return list_topics

def create_commentary_topic_forum(id, commentary, author):
    """
    Fonction qui créée et ajoute un commentaire sur un Topic
    : param id (str) : ID du Topic
    : param commentary (str) : Le commentaire
    : param author (str) : L'auteur du commentaire
    """
    topic = get_topic_forum(id)
    date = get_date()

    id_commentary = create_id(author, date)
    struc_commentary = {
        "id" : id_commentary[0:10],
        "auteur" : author,
        "date" : date,
        "commentaire" : commentary
        }

    topic["commentary"].append(struc_commentary)

    forums_topics.update_one({"id" : id}, {"$set": {"commentary" : topic["commentary"]}});

def modify_topic_forum(id, title, categorie, content):
    """
    Fonction qui modifie un topic dans la BDD
    : param id (str) : id du topic
    : param title (str) : Titre du topic
    : param categorie (str) : Categorie du topic
    : param content (str) : Contenu du topic
    """
    date = get_date()

    topic = forums_topics.find_one({"id" : id})

    topic["title"] = title
    topic["categorie"] = categorie
    topic["content"] = content

    forums_topics.update_one({"id" : id}, {"$set": { "title" : topic["title"], "categorie" : topic["categorie"], "content" : topic["content"]}});


#create_user(True, "thomas", "dlmp", "test@test.fr", "virtux", "test")