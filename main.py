import os
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request, abort
from flask_bootstrap import Bootstrap5
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, db

from classes import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

PRIVATE_KEY_MID = os.environ.get('PRIVATE_KEY')
PRIVATE_KEY = '-----BEGIN PRIVATE KEY-----\n' + PRIVATE_KEY_MID + '\n-----END PRIVATE KEY-----'

# Initialize Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": PRIVATE_KEY,
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL')
})
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bioaddmedknowledgebase-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/')

api = Api(app)


def login_required(f):
    """
    Decorator that checks if user is logged in.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('give_password'))
        return f(*args, **kwargs)

    return wrapper


def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Auth-Key') is None:
            abort(401)
        password = ref.child('password').get()
        if not password or not check_password_hash(password, request.headers.get('Auth-Key')):
            abort(401)
        return view_function(*args, **kwargs)

    return decorated_function


class ArticleListResource(Resource):
    method_decorators = [require_api_key]

    @staticmethod
    def get():
        articles = ref.child('articles').get()
        return jsonify({'articles': [article for article in articles.values()]})


api.add_resource(ArticleListResource, '/api/articles')


@app.route('/', methods=["GET", "POST"])
def give_password():
    form = GivePasswordForm()
    if form.validate_on_submit():
        password = str(ref.child('password').get())
        if password and check_password_hash(password, form.password.data):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Niepoprawne hasło!", "info")
            return redirect(url_for('give_password'))

    return render_template("index.html", form=form, is_login_page=True)


@app.route('/add_password', methods=["GET", "POST"])
def add_password():
    form = AddPasswordForm()
    if form.validate_on_submit():
        existing_password = ref.child('password').get()
        if existing_password is None:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            ref.child('password').set(hash_and_salted_password)
            return redirect(url_for('give_password'))
        else:
            flash("Hasło już istnieje!", "info")
            return redirect(url_for('give_password'))
    return render_template("add_password.html", form=form)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    form = CheckArticleForm()
    if form.validate_on_submit():
        if form.doi.data:
            articles = ref.child('articles').get()
            article = next((a for a in articles.values() if a['doi'] == form.doi.data), None)
            if article:
                flash("Artykuł już istnieje!")
            else:
                flash("Nie znaleziono artykułu!")
        return redirect(url_for('home'))
    if not ref.child('articles').get():
        number_of_articles = 0
    else:
        number_of_articles = len(ref.child('articles').get())
    return render_template("home.html", form=form, number_of_articles=number_of_articles)


@app.route('/add_article', methods=["GET", "POST"])
@login_required
def add_article():
    form = AddArticleForm()
    if form.validate_on_submit():
        full_name = f"{(form.first_name.data.capitalize())} {form.last_name.data.capitalize()}"
        article = Article(
            link=form.link.data,
            year=form.year.data,
            category=form.category.data,
            title=form.title.data,
            problem_description=form.problem_description.data,
            solution_description=form.solution_description.data,
            result=form.result.data,
            problems=form.problems.data,
            additional_notes=form.additional_notes.data,
            doi=form.doi.data,
            full_name=full_name
        )
        ref.child('articles').push(article.to_dict())
        return redirect(url_for('home'))
    return render_template("add_article.html", form=form)


@app.route('/articles', methods=["GET", "POST"])
@login_required
def show_articles():
    form = SortForm()
    if form.validate_on_submit():
        articles = ref.child('articles').get()
        if form.sort_by.data == 'addition_date':
            articles = sorted(articles.values(), key=lambda x: x['addition_date'], reverse=not form.ascending.data)
        elif form.sort_by.data == 'year':
            articles = sorted(articles.values(), key=lambda x: x['year'], reverse=not form.ascending.data)
        elif form.sort_by.data == 'title':
            articles = sorted(articles.values(), key=lambda x: x['title'], reverse=not form.ascending.data)

        if form.category.data:
            articles = [article for article in articles if form.category.data in article['category']]
        return render_template("articles.html", articles=articles, form=form)
    else:
        articles = sorted(ref.child('articles').get().values(), key=lambda x: x['addition_date'], reverse=True)
    return render_template("articles.html", articles=articles, form=form)


if __name__ == "__main__":
    app.run(debug=False)
