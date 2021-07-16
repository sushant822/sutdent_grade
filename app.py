from flask import Flask, render_template, redirect, url_for
from flask import request
#from sklearn.linear_model import LogisticRegression
import joblib
from joblib import load
import pandas as pd
import numpy as np
#import os
#import pickle

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
    #__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #filename = open(os.path.join(__location__, 'StudentGrade.pkl'), errors="ignore")
    filename = 'https://github.com/sushant822/sutdent_grade/blob/main/StudentGrade.sav'

    joblib_LR_model = joblib.load(filename)
    #with open(filename, 'rb') as file:  
    #    Pickled_LR_Model = pickle.load(file)

    test_data = [[studytime, failures, freetime, absences, health, grade_1, grade_2]]

    #test_data = np.array(test_data)
    
    #reshape array
    #test_data = test_data.reshape(1,-1)

    Ypredict_full = joblib_LR_model.predict(test_data)
    #Ypredict = Pickled_LR_Model.predict(test_data)

    #Ypredict = 15

    Ypredict_r = np.round_(Ypredict_full, 2)
    Ypredict = Ypredict_r[0]

    #open file
    #filename = open("/Users/sdeshpande/Desktop/Sushant/Temp/Files/DS/GitHub Desktop/GitHub/sutdent_grade/StudentGrade.pkl","rb")
    
    #load trained model
    #trained_model = joblib.load(filename)
    
    #predict
    #prediction = trained_model.predict(test_data)

    #predict = prediction

    return render_template("index.html", Ypredict_display=Ypredict)
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)