from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField,TextAreaField
from wtforms.validators import DataRequired


class AddArticleForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    year = IntegerField('Rok', validators=[DataRequired()])
    category = StringField('Kategoria', validators=[DataRequired()])
    title = StringField('Tytuł', validators=[DataRequired()])
    problem_description = TextAreaField('Opis problemu', validators=[DataRequired()])
    solution_description = TextAreaField('Opis rozwiązania', validators=[DataRequired()])
    result = TextAreaField('Wynik', validators=[DataRequired()])
    problems = TextAreaField('Problemy', validators=[DataRequired()])
    additional_notes = TextAreaField('Dodatkowe uwagi', validators=[DataRequired()])
    submit = SubmitField('Dodaj artykuł')


class AddPasswordForm(FlaskForm):
    password = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Dodaj hasło')


class GivePasswordForm(FlaskForm):
    password = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class SortForm(FlaskForm):
    sort_by = SelectField('Sortuj po', choices=[
        ('addition_date', 'Data dodania'),
        ('year', 'Rok artykułu'),
        ('category', 'Kategoria'),
        ('title', 'Tytuł')
    ])
    ascending = BooleanField('Rosnąco')
    submit = SubmitField('Sortuj')


class CheckArticleForm(FlaskForm):
    link =  StringField('Link artykułu')
    title = StringField('Tytuł artykułu')
    submit = SubmitField('Sprawdź')
