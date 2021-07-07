from flask import Flask, render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy
#import psycopg2
from flask import request
import joblib
#import pgeocode
#import pandas as pd
import numpy as np
#import requests
#from bs4 import BeautifulSoup
#import time
#from math import sin, cos, sqrt, atan2, radians
#import re
import os
#from tensorflow import keras

app = Flask(__name__)

#db = SQLAlchemy()


@app.route("/")
def home():
    
    return render_template("index.html")



@app.route("/houseprice")
def house_price():
    
    return render_template("houseprice.html")

@app.route("/houseprice",methods=['POST'])
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
    filename = open(os.path.join(__location__, 'StudentGrade.sav'), errors="ignore")
    #filename = 'StudentGrade.sav'

    joblib_model = joblib.load(filename)

    test_data = [[studytime, failures, freetime, absences, health, grade_1, grade_2]]

    Ypredict_full = joblib_model.predict(test_data)
    Ypredict = np.round_(Ypredict_full, 2)

    return render_template("houseprice.html", Ypredict=10)
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)