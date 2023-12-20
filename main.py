import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request, abort
from flask_bootstrap import Bootstrap5
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

from classes import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db.init_app(app)
api = Api(app)


def require_api_key(view_function):
    """
    Decorator that add requirement of key to access api.
    """
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Auth-Key') is None:
            abort(401)
        password = Password.query.filter_by(id=1).first()
        if not password or not check_password_hash(password.value, request.headers.get('Auth-Key')):
            abort(401)
        return view_function(*args, **kwargs)

    return decorated_function


class ArticleListResource(Resource):
    """
    Class that allows to get all articles from api.
    """
    method_decorators = [require_api_key]

    @staticmethod
    def get():
        """
        Method that allows to get all articles from api.
        :return: all articles from database
        """
        articles = Article.query.all()
        return jsonify({'articles': [article.to_dict() for article in articles]})


api.add_resource(ArticleListResource, '/api/articles')

with app.app_context():
    db.create_all()


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


@app.route('/', methods=["GET", "POST"])
def give_password():
    """
    Allows to log in to the website.
    """
    form = GivePasswordForm()
    if form.validate_on_submit():
        password = Password.query.filter_by(id=1).first()
        if password and check_password_hash(password.value, form.password.data):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Niepoprawne hasło!","info")
            return redirect(url_for('give_password'))

    return render_template("index.html", form=form, is_login_page=True)


@app.route('/add_password', methods=["GET", "POST"])
def add_password():
    """
    Allows to add only one password to the website.
    """
    form = AddPasswordForm()
    if form.validate_on_submit():
        existing_password = Password.query.first()
        if existing_password is None:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_password = Password(value=hash_and_salted_password)
            db.session.add(new_password)
            db.session.commit()
            return redirect(url_for('give_password'))
        else:
            flash("Hasło już istnieje!", "info")
            return redirect(url_for('give_password'))
    return render_template("add_password.html", form=form)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    """
    Allows to check if article with given doi exists in database.
    """
    form = CheckArticleForm()
    if form.validate_on_submit():
        if form.doi.data:
            article = Article.query.filter_by(doi=form.doi.data).first()
            if article:
                flash("Artykuł już istnieje!")
            else:
                flash("Nie znaleziono artykułu!")
        return redirect(url_for('home'))
    number_of_articles = len(Article.query.all())
    return render_template("home.html", form=form, number_of_articles=number_of_articles)


@app.route('/add_article', methods=["GET", "POST"])
@login_required
def add_article():
    """
    Allows to add new article to the website.
    """
    form = AddArticleForm()
    if form.validate_on_submit():
        full_name = f"{(form.first_name.data.capitalize())} {form.last_name.data.capitalize()}"
        user = User.query.filter_by(username=full_name).first()
        if not user:
            user = User(username=full_name)
            db.session.add(user)
            db.session.commit()
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
            addition_date=datetime.now(),
            user_id=user.id,
            doi=form.doi.data,
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_article.html", form=form)


@app.route('/articles', methods=["GET", "POST"])
@login_required
def show_articles():
    """
    Allows to show all articles and sort them by addition date, year or title.
    Also allows to filter articles by category.
    """
    form = SortForm()
    if form.validate_on_submit():
        order = db.desc if not form.ascending.data else db.asc
        if form.sort_by.data == 'addition_date':
            articles = Article.query.order_by(order(Article.addition_date))
        elif form.sort_by.data == 'year':
            articles = Article.query.order_by(order(Article.year))
        elif form.sort_by.data == 'title':
            articles = Article.query.order_by(order(Article.title))
        else:
            articles = Article.query

        if form.category.data:
            articles = [article for article in articles if form.category.data in article.category]
        else:
            articles = articles.all()

        return render_template("articles.html", articles=articles, form=form)
    else:
        articles = Article.query.order_by(Article.addition_date.desc()).all()
    return render_template("articles.html", articles=articles, form=form)


if __name__ == "__main__":
    app.run(debug=True)
