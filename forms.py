from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectMultipleField, FieldList, FormField, TimeField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_ckeditor import CKEditorField


class AddArticleForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    year = IntegerField('Rok', validators=[DataRequired()])
    category = StringField('Kategoria', validators=[DataRequired()])
    title = StringField('Tytuł', validators=[DataRequired()])
    problem_description = StringField('Opis problemu', validators=[DataRequired()])
    solution_description = StringField('Opis rozwiązania', validators=[DataRequired()])
    result = StringField('Wynik', validators=[DataRequired()])
    problems = StringField('Problemy', validators=[DataRequired()])
    additional_notes = StringField('Dodatkowe uwagi', validators=[DataRequired()])
    submit = SubmitField('Dodaj artykuł')


class AddPasswordForm(FlaskForm):
    value = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Dodaj hasło')


class GivePasswordForm(FlaskForm):
    password = StringField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

