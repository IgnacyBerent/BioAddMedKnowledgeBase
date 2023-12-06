import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash

from classes import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db.init_app(app)

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
            flash("Niepoprawne hasło!")
            return redirect(url_for('give_password'))

    return render_template("index.html", form=form)


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
            flash("Hasło już istnieje!")
            return redirect(url_for('give_password'))
    return render_template("add_password.html", form=form)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    """
    Allows to check if article with given link or title exists.
    """
    form = CheckArticleForm()
    if form.validate_on_submit():
        if form.link.data and form.title.data:
            flash("Proszę wypełnić tylko jedno pole!")
        elif form.link.data:
            article = Article.query.filter_by(link=form.link.data).first()
            if article:
                flash("Artykuł o podanym linku JUŻ ISTNIEJE!")
            else:
                flash("Artykuł o podanym linku NIE istnieje!")
        elif form.title.data:
            article = Article.query.filter_by(title=form.title.data).first()
            if article:
                flash("Artykuł o podanym tytule JUŻ ISTNIEJE!")
            else:
                flash("Artykuł o podanym tytule NIE istnieje!")
        else:
            flash("Proszę wypełnić jedno z pól!")
    return render_template("home.html", form=form)


@app.route('/add_article', methods=["GET", "POST"])
@login_required
def add_article():
    """
    Allows to add new article to the website.
    """
    form = AddArticleForm()
    if form.validate_on_submit():
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
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_article.html", form=form)


@app.route('/articles', methods=["GET", "POST"])
@login_required
def show_articles():
    """
    Allows to show all articles and sort them by addition date, year, category or title.
    """
    form = SortForm()
    if form.validate_on_submit():
        order = db.desc if not form.ascending.data else db.asc
        if form.sort_by.data == 'addition_date':
            articles = Article.query.order_by(order(Article.addition_date)).all()
        elif form.sort_by.data == 'year':
            articles = Article.query.order_by(order(Article.year)).all()
        elif form.sort_by.data == 'category':
            articles = Article.query.order_by(order(Article.category)).all()
        elif form.sort_by.data == 'title':
            articles = Article.query.order_by(order(Article.title)).all()
        else:
            articles = Article.query.all()
        return render_template("articles.html", articles=articles, form=form)
    else:
        articles = Article.query.order_by(Article.addition_date.desc()).all()
    return render_template("articles.html", articles=articles, form=form)


if __name__ == "__main__":
    app.run(debug=True)
