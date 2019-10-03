import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<startdate><br/>"
        f"/api/v1.0/startend<startandenddate><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query 
    results = (session.query(Measurement.date, Measurement.prcp)).all()

    session.close()

    # Convert list of tuples into normal list
    precip_dict = list(np.ravel(results))

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Return a JSON list of stations from the dataset.
    station = session.query(Station.name).order_by(Station.name).all()

    session.close()

    stations = list(np.ravel(station))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Return query for temperature observations from a year from the last data point.
    tobs =  session.query(Measurement.tobs).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    session.close()

    tob = list(np.ravel(tobs))

    return jsonify(tob)


    #`/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/start<startdate>")
def startdate(startdate):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    tmin_tavg_tmax = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all()

    session.close()

  

    return jsonify(tmin_tavg_tmax)

@app.route("/api/v1.0/startend<startdate><enddate>")
def startandenddate(startdate, enddate):
    session = Session(engine)

    
    # start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate).filter(func.strftime("%Y-%m-%d", Measurement.date) <= enddate).all()

    session.close()

    return jsonify(startend)


if __name__ == "__main__":
    app.run(debug=True)
