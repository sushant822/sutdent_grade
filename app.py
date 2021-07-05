from flask import Flask, render_template, jsonify, url_for
#from flask_sqlalchemy import SQLAlchemy
#import psycopg2
from flask import request
import joblib
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
#from tensorflow import keras

app = Flask(__name__)

#db = SQLAlchemy()

@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/index",methods=['POST'])
def getvalues():
    studytime = request.form['studytime']
    failures = request.form['failures']
    freetime = request.form['freetime']
    absences = request.form['absences']
    health = request.form['health']
    grade_1 = request.form['grade_1']
    grade_2 = request.form['grade_2']

    ###### Convert to numeric ######
    studytime = int(studytime)
    failures = int(failures)
    freetime = int(freetime)
    absences = float(absences)
    health = int(health)
    grade_1 = float(grade_1)
    grade_2 = int(grade_2)

    ###### ML Model ######
    filename = 'LogisticRegression.sav'

    joblib_LR_model = joblib.load(filename)

    test_data = [[studytime, failures, freetime, absences, health, grade_1, grade_2]]

    Ypredict_full = joblib_LR_model.predict(test_data)
    Ypredict = np.round_(Ypredict_full, 2)

    return render_template("index.html", Ypredict=[Ypredict])
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)