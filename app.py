from nis import cat
from flask import *
from flaskext.markdown import Markdown
import functions
import form

app = Flask(__name__)
app.secret_key = '09c1a7ae6fe0c8355f2041414167e7aeb3bc1afc43be7361fa514f044a2ba4d9'
Markdown(app)

def islogged():
    try:
        if session['mail'] != None:
            return True
        else:
            return False
    except:
        return False

def isadmin():
    try:
        if session['is_admin']:
            return True
        else:
            return False
    except:
        return False

@app.route('/')
def home():
    all_blogpost = functions.get_all_postblog()
    if len(all_blogpost) > 3:
        all_blogpost = all_blogpost[0:3]
    return render_template('index.html', posts = all_blogpost)

@app.route("/admin")
def adminHome():
    if isadmin():
        list_users = functions.get_all_user()
        list_postblog = functions.get_all_postblog()
        list_topicforum = functions.get_all_topic_forum()
        return render_template('admin/index.html', title='Tableau de bord', nb_users=len(list_users), nb_postblog = len(list_postblog), nb_forumtopics = len(list_topicforum))
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    formulaire = form.Login()

    # Formulaire envoyé ?
    if formulaire.validate_on_submit():
        mail = formulaire.data["mail"]
        password = formulaire.data['password']

        # Utilisateur inscrit ?
        if functions.verify_user(mail, password):
            infos_user = functions.get_info_user(mail)

            session['is_logged'] = True
            session['mail'] = infos_user["mail"]
            session['prenom'] = infos_user["prenom"]
            session['nom'] = infos_user["nom"]
            session['pseudo'] = infos_user["pseudo"]

            if infos_user["role"] == 1:
                session['is_admin'] = True
            return redirect(url_for('home'))
        else:
            error = 'Adresse mail / Mot de passe incorrect !'

    # Deja connecter ?
    try:
        if session['is_logged'] == True:
            return redirect(url_for('home'))
    except:
        return render_template('/login.html', title='Connexion', error = error, formulaire = formulaire)

@app.route("/logout")
def logout():
    if islogged():
        session.clear()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
@app.route("/admin/blog")
def admin_index_postblog():
    if isadmin():
        all_post = functions.get_all_postblog()
        return render_template('admin/blog/index_postblog.html', title="Blog", all_post = all_post)
    else:
        return redirect(url_for('adminlogin'))

@app.route("/admin/blog/create_postblog", methods=['GET', 'POST'])
def admin_create_postblog():
    if isadmin():
        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"

        if request.method == 'POST':
            post_title = request.form['post_title']
            post_url_img = request.form['post_url_img']
            post_content = "\n" + request.form['post_content']
            functions.create_postblog(post_title, post_url_img, post_content, session["pseudo"])
            message = "Le post a bien été publié !"
            type_message = alerte_green
            return render_template('admin/blog/create_postblog.html', title='Créer un Post', message = message, type_message = type_message)
        return render_template('admin/blog/create_postblog.html', title='Créer un Post')
    else:
        return redirect(url_for('adminlogin'))
    
@app.route("/admin/blog/modify_postblog/<id>", methods=['GET', 'POST'])
def modify_postblog(id):
    if isadmin():
        post = functions.get_postblog(id)
        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"

        if request.method == 'POST':
            post_title = request.form['post_title']
            post_url_img = request.form['post_url_img']
            post_content = request.form['post_content']
            functions.modify_postblog(id, post_title, post_url_img, post_content)
            message = "Le post a bien été modifié !"
            type_message = alerte_green
            post = functions.get_postblog(id)
            return render_template('admin/blog/modify_postblog.html', title='Modifier un Post', post = post, message = message, type_message = type_message)
        return render_template('admin/blog/modify_postblog.html', title='Modifier un Post', post = post)
    else:
        return redirect(url_for('adminlogin'))

@app.route("/blog/postblog/<id>", methods=['GET', 'POST'])
def postblog(id):
    post = functions.get_postblog(id)
    title = post['title']

    if request.method == 'POST':
        new_commentary = request.form["new_commentary"]
        functions.create_commentary_postblog(id, new_commentary, session["pseudo"])
        post = functions.get_postblog(id)
        return render_template('postblog.html', infos = post, title = title)
    return render_template('postblog.html', infos = post, title = title)

@app.route("/admin/forum")
def admin_index_forum():
    if isadmin():
        all_topics = functions.get_all_topic_forum()
        return render_template('admin/forum/index_forum.html', title="Forum", all_topics = all_topics)
    else:
        return redirect(url_for('adminlogin'))

@app.route("/admin/forum/create_categorie_forum", methods=['GET', 'POST'])
def create_categorie_forum():
    if isadmin():
        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"

        if request.method == 'POST':
            categorie_title = request.form['categorie_title']
            functions.create_categorie_forum(categorie_title, session["pseudo"])
            message = "La catégorie a bien été créée !"
            type_message = alerte_green
            return render_template('admin/forum/create_categorie.html', title='Créer une Catégorie Forum', message = message, type_message = type_message)
        return render_template('admin/forum/create_categorie.html', title='Créer une Catégorie Forum')
    else:
        return redirect(url_for('adminlogin'))

@app.route("/admin/forum/create_topic_forum", methods=['GET', 'POST'])
def admin_create_topic_forum():
    if isadmin():
        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"

        categories = functions.get_all_categories_forum()

        if request.method == 'POST':

            topic_title = request.form['topic_title']
            topic_content = "\n" + request.form['topic_content']
            topic_categorie = request.form['topic_categorie']


            functions.create_topic_forum(topic_title, topic_content, session["pseudo"], topic_categorie)
            message = "Le topic a bien été publié !"
            type_message = alerte_green
            return render_template('admin/forum/create_topic.html', title='Créer un Topic', message = message, type_message = type_message, categories = categories)
        return render_template('admin/forum/create_topic.html', title='Créer un Topic', categories = categories)
    else:
        return redirect(url_for('adminlogin'))

@app.route("/forum/topic_forum/<id>", methods=['GET', 'POST'])
def topic_forum(id):
    topic = functions.get_topic_forum(id)
    title = topic['title']

    if request.method == 'POST':
        new_commentary = "\n" + request.form["new_commentary"]
        functions.create_commentary_topic_forum(id, new_commentary, session["pseudo"])
        topic = functions.get_topic_forum(id)
        return render_template('topic_forum.html', topic = topic, title = title)
    return render_template('topic_forum.html', topic = topic, title = title)

@app.route("/admin/forum/modify_topic_forum/<id>", methods=['GET', 'POST'])
def modify_topic_forum(id):
    if isadmin():

        topic = functions.get_topic_forum(id)
        categories = functions.get_all_categories_forum()

        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"


        if request.method == 'POST':
            topic_title = request.form['topic_title']
            topic_content = "\n" + request.form['topic_content']
            topic_categorie = request.form['topic_categorie']

            functions.modify_topic_forum(id, topic_title, topic_categorie, topic_content)
            message = "Le topic a bien été modifié !"
            type_message = alerte_green
            topic = functions.get_topic_forum(id)
            return render_template('admin/forum/modify_topic_forum.html', title='Modifier un Topic', topic = topic, message = message, type_message = type_message, categories = categories)
        return render_template('admin/forum/modify_topic_forum.html', title='Modifier un Topic', topic = topic, categories = categories)
    else:
        return redirect(url_for('adminlogin'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="404"), 404

@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    formulaire = form.Register()

    # Formulaire envoyé ?
    if formulaire.validate_on_submit():
        nom = formulaire.data["nom"]
        prenom = formulaire.data["prenom"]
        mail = formulaire.data["mail"]
        pseudo = formulaire.data["pseudo"]
        password = formulaire.data['password']

        # Utilisateur inscrit ?
        if functions.verify_user(mail, password):
            error = "Les informations entrée sont déjà utilisées par un autre utilisateur !"
        else:
            functions.create_user(False, nom, prenom, mail, pseudo, password)
            return redirect(url_for('login'))

    # Deja connecter ?
    try:
        if session['is_logged'] == True:
            return redirect(url_for('home'))
    except:
        return render_template('/register.html', title='Inscription', error = error, formulaire = formulaire)

@app.route('/blog')
def blog():
    all_blogpost = functions.get_all_postblog()
    return render_template('/index_blog.html', title="Blog", blogposts = all_blogpost)

@app.route("/forum")
def index_forum():
    all_topics = functions.get_all_topic_forum()
    all_categories = functions.get_all_categories_forum()
    return render_template('/index_forum.html', title="Forum", topics = all_topics, categories = all_categories)

@app.route("/forum/create_topic", methods=['GET', 'POST'])
def create_topic():
    if islogged:
        message = None
        type_message = None
        alerte_red = "alerte-message-r"
        alerte_green = "alerte-message-g"

        all_categories = functions.get_all_categories_forum()

        if request.method == 'POST':

            topic_title = request.form['topic_title']
            topic_content = "\n" + request.form['topic_content']
            topic_categorie = request.form['topic_categorie']

            functions.create_topic_forum(topic_title, topic_content, session["pseudo"], topic_categorie)
            message = "Le topic a bien été publié !"
            type_message = alerte_green
            return redirect(url_for('index_forum'))
        return render_template('/create_topic.html', title="Créer un topic", categories = all_categories)
    else:
        return redirect(url_for('login'))

@app.route('/space_member')
def space_member():
    if islogged():
        user_infos = functions.get_info_user(session['mail'])
        return render_template('/espace_membre.html', title="Votre Espace", user = user_infos)
    else:
        return redirect(url_for('login'))

### Boutique

@app.route("/boutique")
def afficher_boutique():
    articles_boutique = functions.shop_get_all_items()
    return render_template("boutique/boutique.html", articles = articles_boutique)

@app.route("/boutique/<id>", methods=['GET', 'POST'])
def boutique(id):
    article = functions.shop_get_item(int(id))

    return render_template("boutique/article.html", article = article)