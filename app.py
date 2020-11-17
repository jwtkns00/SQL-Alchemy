# Dependencies
import datetime as dt
import numpy as np
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## Set up DataBase
#Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect Database
Base = automap_base()
Base.prepare(engine, reflect = True)

#Table References
measurement = Base.classes.measurement
station = Base.classes.station

#Create Session
session = Session(engine)

#Initialize Flask
app = Flask(__name__)

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates.

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#Set Routes
@app.route("/")
def main():
    """List each available routes"""
    return (
        f"Avaiable Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Recieved request for Precipitation API.")
    last_date_query = session.query(func.max(func.strftime("%Y-%m-%d", measurement.date))).all()
    last_date_string = last_date_query[0][0]
    last_date = dt.datetime.strptime(last_date_string, "%Y-%m-%d")

    first_date = last_date - dt.timedelta(365)

    prcp_data = session.query(func.strftime("%Y-%m-%d", measurement.date), measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", measurement.date) >= first_date).all()

    results_dict = {}
    for result in prcp_data:
        results_dict[result[0]] = result [1]

    return jsonify(results_dict)
    

if __name__ == "__main__":
    app.run(debug = True)
