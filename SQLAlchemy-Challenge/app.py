import datetime
from datetime import date, timedelta
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Getting a list of dates for the last 12 months
base_date = datetime.datetime.strptime("2011-01-01", "%Y-%m-%d")
numdays = 365
date_list = [base_date - datetime.timedelta(days=x) for x in range(0, numdays)]

# Converting them to a list of strings
str_dates = []
for date in date_list:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api.v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api.v1.0/precipitation")
def precipitation():

    # Query precipitation
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))
    
    prcp_data = []
    for day in results:
        prcp_dict = {}
        prcp_dict[day.date] = day.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():

    # Query stations
    results = session.query(Station)

    station_data = []
    for station in results:
        station_dict = {}
        station_dict["Station"] = station.station
        station_dict["Name"] = station.name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query temperatures
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))

    temp_data = []
    for day in results:
        temp_dict = {}
        temp_dict[day.date] = day.tobs
        temp_data.append(temp_dict)

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run()