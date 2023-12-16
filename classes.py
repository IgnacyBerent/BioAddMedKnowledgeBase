from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(250), unique=True, nullable=False)
    category = Column(String(250), nullable=False)
    year = Column(Integer)
    title = Column(String(250), unique=True, nullable=False)
    problem_description = Column(String(250), nullable=False)
    solution_description = Column(String(250), nullable=False)
    result = Column(String(250), nullable=False)
    problems = Column(String(250), nullable=False)
    additional_notes = Column(String(500), nullable=True)
    addition_date = Column(DateTime, nullable=False)
    analysis_author = Column(String(250), nullable=True)
    doi = Column(String(250), nullable=False)

    def to_dict(self):
        return {
            'link': self.link,
            'year': self.year,
            'category': self.category,
            'title': self.title,
            'problem_description': self.problem_description,
            'solution_description': self.solution_description,
            'result': self.result,
            'problems': self.problems,
            'additional_notes': self.additional_notes,
            'addition_date': self.addition_date.isoformat(),
            'analysis_author': self.analysis_author,
            'doi': self.doi,
        }


class Password(db.Model):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(250))
