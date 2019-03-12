from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# your code starts here
app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smt203user:password@localhost:5432/smt203test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Review, Course
# your code ends here
if __name__ == '__main__':
    app.run(debug=True)