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
Station = Base.classes.station

#Create Session
session = Session(engine)

#Initialize Flask
app = Flask(__name__)

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates.

def calc_temps(start_date, end_date):
    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

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
        f"/api/v1.0/<start>/<end>"
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

@app.route("/api/v1.0/stations")
def stations():

    print("Received request for Stations API.")

    station_query = session.query(Station.station).all()
    station_list = list(np.ravel(station_query))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    print("Received request for TOBS API.")

    last_date_query = session.query(func.max(func.strftime("%Y-%m-%d", measurement.date))).all()
    last_date_string = last_date_query[0][0]
    last_date = dt.datetime.strptime(last_date_string, "%Y-%m-%d")

    first_date = last_date - dt.timedelta(365)

    results = session.query(measurement).filter(func.strftime("%Y-%m-%d", measurement.date) >= first_date).all()

    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict['date'] = result.station
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Received request for Start Date API.")

    last_date_query = session.query(func.max(func.strftime("%Y-%m-%d", measurement.date))).all()
    last_date = last_date_query[0][0]

    temps = calc_temps(start, last_date)

    return_list = []
    date_dict = {'start_date': start, 'end_date': last_date}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})


    return jsonify(return_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Received request for Start and End Date API.")

    temps = calc_temps(start, end)

    return_list = []
    date_dict = {'start_date': start, 'end_date': end}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(return_list)
if __name__ == "__main__":
    app.run(debug = True)
