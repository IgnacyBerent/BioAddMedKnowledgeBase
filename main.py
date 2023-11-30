from flask import Flask, abort, render_template, redirect, url_for, flash, request
from functools import wraps
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from classes import db, Article, Password
from forms import AddArticleForm, AddPasswordForm, GivePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
ckeditor = CKEditor(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def give_password():
    form = GivePasswordForm()
    if form.validate_on_submit():
        password = Password.query.filter_by(id=0)
        if check_password_hash(password, form.password.data):
            return redirect(url_for('home'))
        else:
            flash("Niepoprawne hasło!")
            return redirect(url_for('give_password'))

    return render_template("index.html")


@app.route('/add_password', methods=["GET", "POST"])
def add_password():
    form = AddPasswordForm()
    if form.validate_on_submit():
        password = Password(value=form.value.data)
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        db.session.add(hash_and_salted_password)
        db.session.commit()
        return redirect(url_for('give_password'))
    return render_template("add_password.html", form=form)


@app.route('/home')
def home():
    articles = Article.query.all()
    return render_template("home.html", articles=articles)


@app.route('/add_article', methods=["GET", "POST"])
def add_article():
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
            additional_notes=form.additional_notes.data
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_article.html", form=form)


@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template("articles.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)