from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
# your code starts here
app = Flask(__name__)
app.debug = True

#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://smt203t1:smt203t1@localhost:5432/smt203project"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Professor, Course, Prof_Course, Review

@app.route("/postprofessor", methods=["POST"])
def create_prof():
    name = request.json["name"]
    new_prof = Professor(name=name)
    db.session.add(new_prof)
    db.session.commit()
    return jsonify("{} was created".format(new_prof))


@app.route("/postcourse", methods=["POST"])
def create_course():
    cid = request.json["cid"]
    name = request.json["name"]
    school = request.json["school"]
    new_course = Course(cid=cid, name=name, school=school)
    db.session.add(new_course)
    db.session.commit()
    return jsonify("{} was created".format(new_course))


@app.route("/postprofcourse", methods=["POST"])
def create_profcouse():
    cname = request.json["cname"]
    pname = request.json["pname"]
    new_profcourse = Prof_Course(cname=cname, pname=pname)
    db.session.add(new_profcourse)
    db.session.commit()
    return jsonify("{} was created".format(new_profcourse))


@app.route("/postreview", methods=["POST"])
def create_postreview():
    reviewer = request.json["reviewer"]
    pname = request.json["pname"]
    cname = request.json["cname"]
    score1 = request.json["score1"]
    score2 = request.json["score2"]
    score3 = request.json["score3"]
    try:
        year = request.json["year"]
    except:
        year = None
    try:
        school = request.json["school"]
    except:
        school = None
    try:
        comment = request.json["comment"]
    except:
        comment = None
    try:
        advice = request.json["advice"]
    except:
        advice = None
    new_review = Review(reviewer=reviewer, pname=pname, cname=cname, score1=score1,
                        score2=score2, score3=score3, year=year, school=school, comment=comment, advice=advice)
    db.session.add(new_review)
    db.session.commit()
    return jsonify("{} was created".format(new_review))

#######################GET Method######################################

@app.route("/getcourse",methods=["GET"])
def get_course():
    if 'cid' in request.args:
        cid = request.args.get("cid")
        course = Course.query.filter_by(cid=cid).all()
        return jsonify([c.serialize() for c in course])
    elif 'cname' in request.args:
        cname = request.args.get("cname")
        course = Course.query.filter_by(name=cname).all()
        return jsonify([c.serialize() for c in course])

@app.route("/getprofessor",methods=['Get'])
def get_professor():
    name = request.args.get("name")
    professor = Professor.query.filter(Professor.name.like('%'+name+'%')).all()
    return jsonify([p.serialize() for p in professor])
        
@app.route("/getreview", methods=["GET"])
def get_review():
    if "cid" in request.args:  # if user enter courseID
        cid = request.args.get("cid")
        course = Course.query.filter_by(cid=cid).first()
        cname = course.name
    else:  # if user enter course name
        cname = request.args.get("cname")
    if "offset" in request.args:  # if user specifiy how many records to show
        offset = request.args.get("offset")
        review = Review.query.filter_by(cname=cname).limit(offset)
        return jsonify([r.serialize() for r in review])
    else:
        review = Review.query.filter_by(cname=cname).limit(15)
        return jsonify([r.serialize() for r in review])

@app.route("/getprofcourse",methods=["GET"])
def get_profcourse():
    if "cid" in request.args:
        cid = request.args.get("cid")
        course = Course.query.filter_by(cid=cid).first()
        cname = course.name
        profcourse = Prof_Course.query.filter_by(cname=cname).all()
        return jsonify([p.serialize() for p in profcourse])
    elif "cname" in request.args:
        cname = request.args.get("cname")
        profcourse = Prof_Course.query.filter_by(cname=cname).all()
        return jsonify([p.serialize() for p in profcourse])
    elif "pname" in request.args:
        pname = request.args.get("pname")
        profcourse = Prof_Course.query.filter_by(pname=pname).all()
        return jsonify([p.serialize() for p in profcourse])


@app.route("/getmodreview", methods=["GET"])
def get_modreview():
    pname = request.args.get("pname")
    if "cname" in request.args:
        cname = request.args.get("course_name")  # enter course name
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialize() for r in review])
    elif "cid" in request.args:  # enter courseID
        cid = request.args.get("cid")
        course = Course.query.filter_by(cid=cid).first()
        cname = course.name
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialize() for r in review])
    else:
        review = Review.query.filter_by(pname=pname)
        return jsonify([r.serialize() for r in review])


@app.route("/getfilterscore", methods=["GET"])
def get_filterscore():
    if "desc" in request.args and request.args.get("desc") == "False":
        if 'avgscore1' in request.args:
            avgscore1 = request.args.get("avgscore1")
        else:
            avgscore1 = 5
        if 'avgscore2' in request.args:
            avgscore2 = request.args.get("avgscore2")
        else:
            avgscore2 = 5
        if 'avgscore3' in request.args:
            avgscore3 = request.args.get("avgscore3")
        else:
            avgscore3 = 5
        if "cid" in request.args:
            cid = request.args.get("cid")
            course = Course.query.filter_by(cid=cid)
            cname = course.name
        else:
            cname = request.args("cname")
        temp = Review.query.with_entities(Review.cname,Review.pname).\
            group_by(Review.cname,Review.pname).\
                having(db.and_(db.func.avg(Review.score1) <= avgscore1,
                db.func.avg(Review.score2) <= avgscore2,
                db.func.avg(Review.score3) <= avgscore3)).subquery()
        review = Review.query.filter(Review.cname==temp.c.cname,Review.pname==temp.c.pname,Review.cname==cname)
        return jsonify([r.serialize() for r in review])
    else:
        if 'avgscore1' in request.args:
            avgscore1 = request.args.get("avgscore1")
        else:
            avgscore1 = 0
        if 'avgscore2' in request.args:
            avgscore2 = request.args.get("avgscore2")
        else:
            avgscore2 = 0
        if 'avgscore3' in request.args:
            avgscore3 = request.args.get("avgscore3")
        else:
            avgscore3 = 0
        if "cid" in request.args:
            cid = request.args.get("cid")
            course = Course.query.filter_by(cid=cid).first()
            cname = course.name
        else:
            cname = request.args.get("cname")
        temp = Review.query.with_entities(Review.cname,Review.pname).\
            group_by(Review.cname,Review.pname).\
                having(db.and_(db.func.avg(Review.score1) >= avgscore1,
                db.func.avg(Review.score2) >= avgscore2,
                db.func.avg(Review.score3) >= avgscore3)).subquery()
        review = Review.query.filter(Review.cname==temp.c.cname,Review.pname==temp.c.pname,Review.cname==cname)
        return jsonify([r.serialize() for r in review])


@app.route("/getall", methods=["GET"])
def get_all():
    school = request.args.get("school")
    if "offset" in request.args:  # if user specifiy how many records to show
        offset=request.args.get("offset")
        course=Course.query.filter_by(school=school).limit(offset)
        return jsonify([c.serialize() for c in course])
    else:
        course=Course.query.filter_by(school=school).limit(15)
        return jsonify([c.serialize() for c in course])

# your code ends here
if __name__ == "__main__":
    app.run(debug=True)
