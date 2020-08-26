## Step 2 - Climate App

#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement

station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start_date>/<br/>"
        f"/api/v1.0/start_to_end/<start>&<end>/"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()


    prcp_values = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_values.append(prcp_dict)

    return jsonify(prcp_values)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    

    results = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281', measurement.date > '2016-08-23').\
        order_by(measurement.date).all()
    
    session.close()

    most_active = list(np.ravel(results))

    return jsonify(most_active)


@app.route("/api/v1.0/start/<start_date>/")
def start(start_date):

    starter = dt.datetime.strptime(start_date, "%m-%d-%Y")


    session = Session(engine)

    temps = [measurement.date,
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)]

    results = session.query(*temps).\
    filter(measurement.date >= starter.date()).\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    start_date = list(np.ravel(results))

    return jsonify(start_date)

@app.route("/api/v1.0/start_to_end/<start_date>&<end_date>/")
def start_to_end(start_date, end_date):

    starter = dt.datetime.strptime(start_date, "%m-%d-%Y")
    ender = dt.datetime.strptime(end_date, "%m-%d-%Y")

    session = Session(engine)

    temps = [measurement.date,
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)]

    results = session.query(*temps).\
    filter(measurement.date >= starter.date(), measurement.date <= ender.date()).\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

    start_end = list(np.ravel(results))

    return jsonify(start_end)
    

if __name__ == '__main__':
    app.run(debug=True)



