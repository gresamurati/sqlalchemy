# imports dependencies
###########################################

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# initializes database
###########################################

engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread': False}
)
Base = automap_base()
Base.prepare(engine, reflect=True)

###########################################
# creates references to Measurement
# and Station tables
###########################################

measurement = Base.classes.measurement

station = Base.classes.station

session = Session(engine)

####################################
# initializes Flask app
####################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Hello! Welcome to the climate app API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-10 <br/>"
        f"/api/v1.0/2016-08-10/2016-08-20 <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    results=session.query(measurement.date, measurement.prcp).group_by(measurement.date).all()
    print(results)
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    stations_json = session.query(station.station).all()
    print(stations_json)
    return jsonify(stations_json)


@app.route("/api/v1.0/tobs")     
def active():
    active= session.query(station.name, measurement.date, measurement.tobs).filter(measurement.date >= "2016-08-24", measurement.date <= "2017-08-23").all()
    print(active)

    # creates JSONified list of dictionaries
    tobs_list = []
    for mostactive in active:
        row = {}
        row["Station"] = mostactive[0]
        row["Date"] = mostactive[1]
        row["Temperature"] = int(mostactive[2])
        tobs_list.append(row)

    return jsonify (tobs_list)

@app.route("/api/v1.0/<start>") 
def start_range(start):

    one_date = session.query(measurement.date,func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)) \
             .filter(measurement.date >= start) \
             .group_by(measurement.date).all()
    return jsonify(one_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    two_dates = session.query(measurement.date,func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)) \
             .filter(measurement.date >= start).filter(measurement.date <= end) \
             .group_by(measurement.date).all()
    return jsonify(two_dates)

if __name__ == '__main__':
    app.run(debug=True)
