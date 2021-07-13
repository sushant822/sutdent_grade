from flask import Flask, render_template
from flask import request
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
import numpy as np
import os
import pickle

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
    absences = int(absences)
    health = int(health)
    grade_1 = int(grade_1)
    grade_2 = int(grade_2)

    ###### ML Model ######
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = open(os.path.join(__location__, 'StudentGrade.pkl'), errors="ignore")
    #filename = 'StudentGrade.sav'

    joblib_model = joblib.load(filename)
    #with open(filename, 'rb') as file:  
    #    Pickled_LR_Model = pickle.load(file)

    test_data = [[studytime, failures, freetime, absences, health, grade_1, grade_2]]

    Ypredict = joblib_model.predict(test_data)
    #Ypredict = Pickled_LR_Model.predict(test_data)

    #Ypredict = 15

    #Ypredict = np.round_(Ypredict_full, 2)

    #Ypredict = 20

    return render_template("index.html", Ypredict_display=Ypredict)
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)