from datetime import datetime


class Article:
    def __init__(self, doi, link, category, year, title, problem_description, solution_description, result, problems,
                 additional_notes, full_name):
        self.doi = doi
        self.link = link
        self.category = category
        self.year = year
        self.title = title
        self.problem_description = problem_description
        self.solution_description = solution_description
        self.result = result
        self.problems = problems
        self.additional_notes = additional_notes
        self.addition_date = datetime.now()
        self.full_name = full_name

    def to_dict(self):
        return {
            'doi': self.doi,
            'link': self.link,
            'category': self.category,
            'year': self.year,
            'title': self.title,
            'problem_description': self.problem_description,
            'solution_description': self.solution_description,
            'result': self.result,
            'problems': self.problems,
            'additional_notes': self.additional_notes,
            'addition_date': self.addition_date.isoformat(),
            'user_full_name': self.full_name,
        }
