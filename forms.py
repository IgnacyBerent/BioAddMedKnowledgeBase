from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField, TextAreaField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length


class AddArticleForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    year = IntegerField('Rok', validators=[DataRequired()])
    category = SelectMultipleField('Kategoria', validators=[DataRequired(), Length(max=2)], choices=[
        ('Bio-materiały', 'Bio-materiały'),
        ('Bio-mechanika', 'Bio-mechanika'),
        ('Bio-druk', 'Bio-druk'),
        ('Druk Leków', 'Druk Leków'),
        ('Druk żywności', 'Druk żywności'),
        ('Diagnostyka', 'Diagnostyka'),
        ('Planowanie operacji', 'Planowanie operacji'),
        ('Sztuczne narządy', 'Sztuczne narządy'),
        ('Sztuczne Kości', 'Sztuczne Kości'),
        ('Protezy', 'Protezy'),
        ('Materiały Stalowe', 'Materiały Stalowe'),
        ('Scaffoldy', 'Scaffoldy'),
        ('Inżynieria tkankowa', 'Inżynieria tkankowa'),
        ('Implanty Stomatologiczne', 'Implanty Stomatologiczne'),
        ('Filamenty', 'Filamenty'),
        ('Metaanaliza', 'Metaanaliza'),
        ('Inne', 'Inne')
    ])
    title = StringField('Tytuł', validators=[DataRequired()])
    problem_description = TextAreaField('Opis problemu', validators=[DataRequired()])
    solution_description = TextAreaField('Opis rozwiązania', validators=[DataRequired()])
    result = TextAreaField('Wynik', validators=[DataRequired()])
    problems = TextAreaField('Problemy', validators=[DataRequired()])
    additional_notes = TextAreaField('Dodatkowe uwagi', validators=[DataRequired()])
    first_name = StringField('Imię', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    doi = StringField('DOI', validators=[DataRequired()])
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
        ('title', 'Tytuł')
    ])
    category = SelectField('Kategoria', choices=[
        ('', 'Wszystkie'),
        ('Bio-materiały', 'Bio-materiały'),
        ('Bio-mechanika', 'Bio-mechanika'),
        ('Bio-druk', 'Bio-druk'),
        ('Druk Leków', 'Druk Leków'),
        ('Druk żywności', 'Druk żywności'),
        ('Diagnostyka', 'Diagnostyka'),
        ('Planowanie operacji', 'Planowanie operacji'),
        ('Sztuczne narządy', 'Sztuczne narządy'),
        ('Sztuczne Kości', 'Sztuczne Kości'),
        ('Protezy', 'Protezy'),
        ('Materiały Stalowe', 'Materiały Stalowe'),
        ('Scaffoldy', 'Scaffoldy'),
        ('Inżynieria tkankowa', 'Inżynieria tkankowa'),
        ('Implanty Stomatologiczne', 'Implanty Stomatologiczne'),
        ('Filamenty', 'Filamenty'),
        ('Metaanaliza', 'Metaanaliza'),
        ('Inne', 'Inne')
    ])
    ascending = BooleanField('Rosnąco')
    submit = SubmitField('Sortuj')


class CheckArticleForm(FlaskForm):
    doi = StringField('DOI')
    submit = SubmitField('Sprawdź')
