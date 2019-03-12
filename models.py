from app import db

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    professor = db.Column(db.String(80), primary_key=True)
    school = db.Column(db.String(10), nullable=False)

    def __init__(self,id,name,professor,school):
        self.id = id
        self.name = name
        self.professor = professor
        self.school = school


class Review(db.Model):
    __tablename__ = "review"
    reviewer = db.Column(db.String(80), primary_key=True)
    professor = db.Column(db.String(80), primary_key=True)
    course = db.Column(db.String(80), primary_key=True)
    score1 = db.Column(db.Float, nullable=False)
    score2 = db.Column(db.Float, nullable=False)
    score3 = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer)
    school = db.Column(db.String(10))
    comment = db.Column(db.String(300))
    constraint = db.ForeignKeyConstraint(
        ('professor', 'course'), ('professor_course.professor_id', 'professor_course.course_id'))
    courses = db.relationship('Course',back_populates='review',cascade='all',lazy=True,uselist=True)

    def __init__(self, reviewer, professor, course, score1, score2, score3, year=None, school=None, comment=None):
        self.reviewer = reviewer
        self.professor = professor
        self.course = course
        self.score1 = score1
        self.score2 = score2
        self.score3 = score3
        school = [] if school is None else school
        self.school = school
        year = [] if year is None else year
        self.year = year
        comment = [] if comment is None else comment
        self.comment = comment
