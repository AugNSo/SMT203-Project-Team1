from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# your code starts here
app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://smt203t1:smt203t1@localhost:5432/smt203project"
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
    if 'cid' in request.json:
        cid = request.json["cid"]
        row = Course.query.filter_by(cid=cid).first()
        cname = row.name
        return cname
    elif 'cname' in request.json:
        cname = request.json['cname']
        row = Course.query.filter_by(cname=cname).first()
        cname = row.name
        return cname

@app.route("/getprofessor",methods=['Get'])
def get_professor():
    name = request.json['name']
    professor = Professor.query.filter(Professor.name.like('%'+name+'%')).all()
    return jsonify([p.serialize() for p in professor])
        
@app.route("/getreview", methods=["GET"])
def get_review():
    if "cid" in request.json:  # if user enter courseID
        cid = request.json["cid"]
        for row in Course.query.filter_by(cid=cid):
            cname = row.name
    else:  # if user enter course name
        cname = request.json["cname"]
    if "offset" in request.json:  # if user specifiy how many records to show
        offset = request.json["offset"]
        review = Review.query.filter_by(cname=cname).limit(offset)
        return jsonify([r.serialize() for r in review])

    else:
        review = Review.query.filter_by(cname=cname).limit(15)
        return jsonify([r.serialize() for r in review])


@app.route("/getmodreview", methods=["GET"])
def get_modreview():
    pname = request.json["pname"]
    if "cname" in request.json:
        cname = request.json["course_name"]  # enter course name
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialize() for r in review])
    else:  # enter courseID
        cid = request.json["cid"]
        for row in Course.query.filter_by(cid=cid):
            cname = row.name
        review = Review.query.filter_by(cname=cname, pname=pname)
        return jsonify([r.serialize() for r in review])


@app.route("/getfilterscore", methods=["GET"])
def get_filterscore():
    if "desc" in request.json and request.json["desc"] == "False":
        try:
            avgscore1 = request.json["avgscore1"]
        except:
            avgscore1 = 5
        try:
            avgscore2 = request.json["avgscore2"]
        except:
            avgscore2 = 5
        try:
            avgscore3 = request.json["avgscore3"]
        except:
            avgscore3 = 5
        if "cid" in request.json:
            cid = request.json["cid"]
            for row in Course.query.filter_by(cid=cid):
                cname = row.name
        else:
            cname = request.json["cname"]
        temp = Review.query.with_entities(Review.cname,Review.pname).\
            group_by(Review.cname,Review.pname).\
                having(db.and_(db.func.avg(Review.score1) <= avgscore1,
                db.func.avg(Review.score2) <= avgscore2,
                db.func.avg(Review.score3) <= avgscore3)).subquery()
        review = Review.query.filter(Review.cname==temp.c.cname,Review.pname==temp.c.pname)
        return jsonify([r.serialize() for r in review])
    else:
        try:
            avgscore1 = request.json["avgscore1"]
        except:
            avgscore1 = 0
        try:
            avgscore2 = request.json["avgscore2"]
        except:
            avgscore2 = 0
        try:
            avgscore3 = request.json["avgscore3"]
        except:
            avgscore3 = 0
        if "cid" in request.json:
            cid = request.json["cid"]
            for row in Course.query.filter_by(cid=cid):
                cname = row.name
        else:
            cname = request.json["cname"]
        temp = Review.query.with_entities(Review.cname,Review.pname).\
            group_by(Review.cname,Review.pname).\
                having(db.and_(db.func.avg(Review.score1) >= avgscore1,
                db.func.avg(Review.score2) >= avgscore2,
                db.func.avg(Review.score3) >= avgscore3)).subquery()
        review = Review.query.filter(Review.cname==temp.c.cname,Review.pname==temp.c.pname)
        return jsonify([r.serialize() for r in review])


@app.route("/getall", methods=["GET"])
def get_all():
    school = request.json["school"]
    if "offset" in request.json:  # if user specifiy how many records to show
        offset=request.json["offset"]
        course=Course.query.filter_by(school=school).limit(offset)
        return jsonify([c.serialize() for c in course])
    else:
        course=Course.query.filter_by(school=school).limit(15)
        return jsonify([c.serialize() for c in course])

# your code ends here
if __name__ == "__main__":
    app.run(debug=True)
