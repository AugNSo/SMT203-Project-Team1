from app import db


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    prof_course = db.relationship(
        'Prof_Course', back_populates='course', cascade='all', lazy=True, uselist=True)

    def __init__(self, id, name, professor, school):
        self.id = id
        self.name = name


class Professor(db.Model):
    __tablename__ = "professor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    prof_course = db.relationship(
        'Prof_Course', back_populates='professor', cascade='all', lazy=True, uselist=True)

    def __init__(self, name):
        self.name = name


class Prof_Course(db.Model):
    __tablename__ = "prof_course"
    cid = db.Column(db.String(20), db.ForeignKey(
        'course.id'), primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey(
        'professor.id'), primary_key=True)
    professor = db.relationship('Professor', back_populates='prof_course')
    course = db.relationship('Course', back_populates='prof_course')
    review = db.relationship(
        'Review', back_populates='prof_course', cascade='all', lazy=True, uselist=True)


class Review(db.Model):
    __tablename__ = "review"
    reviewer = db.Column(db.String(80), primary_key=True)
    professor = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(80), primary_key=True)
    score1 = db.Column(db.Float, nullable=False)
    score2 = db.Column(db.Float, nullable=False)
    score3 = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer)
    school = db.Column(db.String(10))
    comment = db.Column(db.String(300))
    advice = db.Column(db.String(300))
    constraint = db.ForeignKeyConstraint(
        ('professor', 'course'), ('professor_course.pid', 'professor_course.cid'))
    prof_course = db.relationship('Prof_Course', back_populates='review')

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
