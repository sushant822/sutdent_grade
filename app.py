from flask import Flask, render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy
#import psycopg2
from flask import request
import joblib
#import pgeocode
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from math import sin, cos, sqrt, atan2, radians
import re
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
    studytime_1 = request.form['studytime']
    failures_1 = request.form['failures']
    freetime_1 = request.form['freetime']
    absences_1 = request.form['absences']
    health_1 = request.form['health']
    grade_1_1 = request.form['grade_1']
    grade_2_1 = request.form['grade_2']

    ###### Convert to numeric ######
    studytime = int(studytime_1)
    failures = int(failures_1)
    freetime = int(freetime_1)
    absences = int(absences_1)
    health = int(health_1)
    grade_1 = int(grade_1_1)
    grade_2 = int(grade_2_1)

    ###### ML Model ######

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    filename = open(os.path.join(__location__, 'StudentGrade.sav'))

    #filename = 'StudentGrade.sav'

    joblib_LR_model = joblib.load(filename)

    test_data = [[studytime, failures, freetime, absences, health, grade_1, grade_2]]

    Ypredict_full = joblib_LR_model.predict(test_data)
    Ypredict = np.round_(Ypredict_full, 2)

    return render_template("houseprice.html", Ypredict=[Ypredict])
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)