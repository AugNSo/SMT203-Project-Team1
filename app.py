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
    cname = request.json['cname']
    pname = request.json['pname']
    new_profcourse = Prof_Course(cname=cname, pname=pname)
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

#######################GET Method######################################

@app.route('/getreview', methods=["GET"])
def get_review():
    if 'cid' in request.args:                       #if user enter courseID
        cid = request.args.get('course_id')
        cname = Course.query.filter_by(cid=cid).first()
    else:                                           #if user enter course name
        cname = request.args.get('course_name')
    if 'offset' in request.args:                    #if user specifiy how many records to show
        offset = int(request.args.get('offset'))
        review = Review.query.filter_by(cname=cname).limit(offset)
    else:
        review = Review.query.filter_by(cname=cname)
        return jsonify([r.serialze() for r in review])

        

@app.route('/getmodreview', methods=["GET"])
def get_modreview():                
    pname = request.args.get('prof_name')
    if 'cname' in request.args:
        cname = request.args.get('course_name')           #enter course name
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialze() for r in review])
    else:                                           #enter courseID
        cid = request.args.get('course_id')
        cname = Course.query.filter_by(cid=cid).first()
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialze() for r in review])

@app.route('/getfilterscore', methods=["GET"])
def get_filterscore():
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    if 'desc' in request.args and request.args.get('desc') == False:
        try:
            avgScore1 = request.args.get('avgScore1')
        except:
            avgScore1 = 5
        try:
            avgScore2 = request.args.get('avgScore2')
        except:
            avgScore2 = 5
        try:
            avgScore3 = request.args.get('avgScore3')
        except: 
            avgScore3 = 5
        try:
            avgTotal = request.args.get('avgTotal')
        except:
            avgTotal = 5

@app.route('/getall', methods=["GET"])
def get_all():
    school = request.args.get('sch')
    if 'offset' in request.args:                    #if user specifiy how many records to show
        offset = int(request.args.get('offset'))
        course = Course.query.filter_by(school=school).limit(offset)
        return json([c.serialze() for c in course)
    else:
        course = Course.query.filter_by(school=school)
        return json([c.serialze() for c in course)

# your code ends here
if __name__ == '__main__':
    app.run(debug=True)
