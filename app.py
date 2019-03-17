from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# your code starts here
app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smt203t1:smt203t1@localhost:5432/smt203project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Professor, Course, Prof_Course, Review

@app.route('/postprofessor', methods=["POST"])
def create_prof():
    name = request.json['name']
    new_prof = Professor(name=name)
    db.session.add(new_prof)
    db.session.commit()
    return jsonify('{} was created'.format(new_prof))


@app.route('/postcourse', methods=["POST"])
def create_course():
    cid = request.json['cid']
    name = request.json['name']
    school = request.json['school']
    new_course = Course(cid=cid, name=name, school=school)
    db.session.add(new_course)
    db.session.commit()
    return jsonify('{} was created'.format(new_course))


@app.route('/postprofcourse', methods=["POST"])
def create_profcouse():
    #cid = request.json['cid']
    #pid = request.json['pid']
    cname = request.json['cname']
    pname = request.json['pname']

    new_profcourse = Prof_Course(cname=cname, pname=pname)
    #new_profcourse = Prof_Course(cid=cid, pid=pid)
    db.session.add(new_profcourse)
    db.session.commit()
    return jsonify('{} was created'.format(new_profcourse))


@app.route('/postreview', methods=["POST"])
def create_postreview():
    reviewer = request.json['reviewer']
    pname = request.json['pname']
    cname = request.json['cname']
    score1 = request.json['score1']
    score2 = request.json['score2']
    score3 = request.json['score3']
    try:
        year = request.json['year']
    except:
        year = None
    try:
        school = request.json['school']
    except:
        school = None
    try:
        comment = request.json['comment']
    except:
        comment = None
    try:
        advice = request.json['advice']
    except:
        advice = None
    new_review = Review(reviewer=reviewer, pname=pname, cname=cname, score1=score1,
                        score2=score2, score3=score3, year=year, school=school, comment=comment, advice=advice)
    db.session.add(new_review)
    db.session.commit()
    return jsonify('{} was created'.format(new_review))


# your code ends here
if __name__ == '__main__':
    app.run(debug=True)
