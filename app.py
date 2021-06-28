from flask import Flask, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask import request
import joblib
import pgeocode
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from math import sin, cos, sqrt, atan2, radians
import re
#from tensorflow import keras

app = Flask(__name__)

db = SQLAlchemy()

# connect to the db
con = psycopg2.connect(
            host="ec2-34-238-26-109.compute-1.amazonaws.com",
            database="d1jfbocoh8eqgo",
            user="hexbstnnfbqjwk",
            password="13f84410f3efc3df8c053dd3452713a5e63bafe4a7dad292256ae514193d2784"
)



def calgary_data_fun():
    cur = con.cursor()

    # execute query
    # cur.execute("SELECT json_agg(t) FROM (SELECT price, bed, full_bath, half_bath, property_area, years_old, distance_downtown, lot_size, basement, garage, walk_score, bike_score, transit_score, house, condo, townhouse FROM listings)t")

    cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary_df AS cl JOIN score_df AS s ON cl.postal_code = s.postal_code JOIN coordinates_df AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000 AND s.walk_score > 5 AND s.bike_score > 0 AND s.transit_score > 0)t")

    calgary_data = cur.fetchall()
    # print(calgary_data)

    # close cursor
    #cur.close()

    # close the connection
    #con.close()

    return calgary_data

def bar_fun():
    cur = con.cursor()

    # execute query
    # cur.execute("SELECT json_agg(t) FROM (SELECT price, bed, full_bath, half_bath, property_area, years_old, distance_downtown, lot_size, basement, garage, walk_score, bike_score, transit_score, house, condo, townhouse FROM listings)t")

    # cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary AS cl JOIN score AS s ON cl.postal_code = s.postal_code JOIN coordinates AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000)t")

    cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary_df AS cl JOIN score_df AS s ON cl.postal_code = s.postal_code JOIN coordinates_df AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000 AND cl.property_type IS NOT null)t")

    bar_data = cur.fetchall()
    # print(calgary_data)

    # close cursor
    #cur.close()

    # close the connection
    #con.close()

    return bar_data

@app.route("/")
def home():

    # create cursor
    cur = con.cursor()

    # execute query
    # cur.execute("SELECT json_agg(t) FROM (SELECT price, bed, full_bath, half_bath, property_area, years_old, distance_downtown, lot_size, basement, garage, walk_score, bike_score, transit_score, house, condo, townhouse FROM listings)t")

    # cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary AS cl JOIN score AS s ON cl.postal_code = s.postal_code JOIN coordinates AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000)t")

    cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary_df AS cl JOIN score_df AS s ON cl.postal_code = s.postal_code JOIN coordinates_df AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000)t")
    
    calgary_data = cur.fetchall()
    # print(calgary_data)

    # close cursor
    #cur.close()

    # close the connection
    #con.close()

    # Return template and data
    return render_template("index.html", calgary=[i for i in calgary_data])



@app.route("/jsonified")
def calgary_data():
    """Return the Calgary data as json"""
    calgary = calgary_data_fun()
    # calgary = calgary[:15]
    return jsonify(calgary)


@app.route("/bardata")
def bar_data():
    bar = bar_fun()
    return jsonify(bar)


@app.route("/viz")
def viz():
    return render_template("viz.html")

@app.route("/scatter")
def scatter():
    return render_template("scatter.html")

@app.route("/bar")
def bar():
    return render_template("bar.html")

@app.route("/data")
def data():
    # create cursor
    cur = con.cursor()

    # execute query
    # cur.execute("SELECT price, bed, full_bath, half_bath, property_area, years_old, distance_downtown, lot_size, basement, garage, walk_score, bike_score, transit_score, house, condo, townhouse FROM listings")

    # cur.execute("SELECT json_agg(t) FROM (SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary AS cl JOIN score AS s ON cl.postal_code = s.postal_code JOIN coordinates AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000)t")

    cur.execute("SELECT cl.price, cl.address, cl.postal_code, cl.bed, cl.full_bath, cl.half_bath, cl.property_area, cl.property_type, s.walk_score, s.bike_score, s.transit_score, coord.lat, coord.long FROM calgary_df AS cl JOIN score_df AS s ON cl.postal_code = s.postal_code JOIN coordinates_df AS coord ON s.postal_code = coord.postal_codes WHERE cl.price < 1000000 AND cl.property_area < 4000")
    
    calgary_data = cur.fetchall()
    # print(calgary_data)

    # close cursor
    #cur.close()

    # close the connection
    #con.close()

    # Return template and data
    return render_template("data.html", calgary=[i for i in calgary_data])

@app.route("/houseprice")
def house_price():
    
    return render_template("houseprice.html")

@app.route("/houseprice",methods=['POST'])
def getvalues():
    bed = request.form['bed']
    full_bath = request.form['full_bath']
    half_bath = request.form['half_bath']
    property_area = request.form['property_area']
    year_built = request.form['year_built']
    lot_size = request.form['lot_size']
    option_basement = request.form['option_basement']
    option_garage = request.form['option_garage']
    property_type = request.form['option_ptype']
    postal_code = request.form['postal_code']

    ###### Property Type ######
    if property_type == 'house':
        house = 1
        condo = 0
        townhouse = 0
    elif property_type == 'condo':
        house = 0
        condo = 1
        townhouse = 0
    else:
        house = 0
        condo = 0
        townhouse = 1
    ####### END ####### 

    ###### Basement #####
    if option_basement == "yes":
        basement = 1
    else:
        basement = 0
    ####### END #######

    ###### Garage ######
    if option_garage == "yes":
        garage = 1
    else:
        garage = 0
    ####### END #######
    
    postal_code = str(postal_code)

    ###### SCRAPE WALKSCORE ######
    scores_walk = []
    scores_bike = []
    scores_transit = []
    for i in postal_code:
        try:
            postal_code_a = i.replace(" ", "%20")
            url_score = "https://www.walkscore.com/score/" + str(postal_code_a)
            # Parse HTML with Beautiful Soup
            response = requests.get(url_score)
            code_soup = BeautifulSoup(response.text, 'html.parser')
            if 'pp.walk.sc/badge/walk/score' in str(code_soup):
                ws = str(code_soup).split('pp.walk.sc/badge/walk/score/')[1][:2].replace('.','')
                scores_walk.append(ws)
            else:
                ws = 0
                scores_walk.append(ws)
            if 'pp.walk.sc/badge/bike/score' in str(code_soup):
                bs = str(code_soup).split('pp.walk.sc/badge/bike/score/')[1][:2].replace('.','')
                scores_bike.append(bs)
            else:
                bs = 0
                scores_bike.append(bs)
            if 'pp.walk.sc/badge/transit/score' in str(code_soup):
                ts = str(code_soup).split('pp.walk.sc/badge/transit/score/')[1][:2].replace('.','')
                scores_transit.append(ts)
            else:
                ts = 0
                scores_transit.append(ts)
        except:
            ws = 0
            scores_walk.append(ws)
            bs = 0
            scores_bike.append(bs)
            ts = 0
            scores_transit.append(ts)
    ####### END #######

    scores_walk_num = scores_walk[0]
    scores_bike_num = scores_bike[0]
    scores_transit_num = scores_transit[0]

    ###### Calculating Distance ######
    country_code = pgeocode.Nominatim('ca')
    coord = country_code.query_postal_code(postal_code)
    x = [coord.latitude, coord.longitude]

    lat1 = radians(x[0])
    lon1 = radians(x[1])
    lat2 = radians(51.0449485)
    lon2 = radians(-114.0739559)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6373.0
    distance_downtown = (R * c)+5
    ####### END #######

    ###### Convert to numeric ######
    bed = int(bed)
    full_bath = int(full_bath)
    half_bath = int(half_bath)
    property_area = float(property_area)
    year_built = int(year_built)
    lot_size = float(lot_size)
    basement = int(basement)
    garage = int(garage)
    walk_score = int(scores_walk_num)
    bike_score = int(scores_bike_num)
    transit_score = int(scores_transit_num)
    house = int(house)
    condo = int(condo)
    townhouse = int(townhouse)

    years_old = 2021 - year_built

    ###### ML Model ######
    filename = 'data/LogisticRegression.sav'

    joblib_LR_model = joblib.load(filename)

    test_data = [[bed, full_bath, half_bath, property_area, years_old, distance_downtown, lot_size, basement, garage, walk_score, bike_score, transit_score, house, condo, townhouse]]

    Ypredict_full = joblib_LR_model.predict(test_data)
    Ypredict = np.round_(Ypredict_full, 2)

    return render_template("houseprice.html", Ypredict=[Ypredict])
    ####### END #######

if __name__ == "__main__":
    app.run(debug=True)