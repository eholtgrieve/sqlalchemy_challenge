# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

engine= create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation analysis of the last 12 months"""
    #Session link from Python to DB
    
    session = Session(engine)
    
    #Query for precipitation
    
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()

    #Storing results in dictionary
    
    precip_list = []
    for date,prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)

    #Return jsonified results of query
    
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the Stations"""
    #Session link from Python to DB

    session = Session(engine)

    #Creating list

    all_Stations = session.query(Station.Station).all()
    all_Stations_list = list(np.ravel(all_Stations))

    #Return jsonified results of query

    return jsonify(all_Stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return list of temperature observations from the most active Station for the previous year"""
    #Session link from Python to DB

    session = Session(engine)

    #Creating query
    most_active = 'USC00519281'
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.Station == most_active).all()
    
    most_active_Station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").filter(Measurement.Station == most_active)

    #Creating list for tobs info
   
    station_tobs = []

    for date,tobs in most_active_Station:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        station_tobs.append(tobs_dict)

    #Return jsonified results of query

    return jsonify(station_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return min,max,avg temperature for specific start date"""
    #Session link from Python to DB

    session = Session(engine)

    #Creating query
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    #Creating list to store query
    
    start_tobs = []
    for min,max,avg in results:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Max"] = max
        start_tobs_dict["Avg"] = avg
        start_tobs.append(start_tobs_dict)
    
    #Return jsonified results of query
    
    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return min,max,avg temperature between specific start and end dates"""
    #Session link from Python to DB
    
    session = Session(engine)

    #Creating query
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    #Creating list to store query
    
    start_end_tobs = []
    for min,max,avg in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["Min"] = min
        start_end_tobs_dict["Max"] = max
        start_end_tobs_dict["Avg"] = avg
        start_end_tobs.append(start_end_tobs_dict)

    #Return jsonified results of query
    
    return jsonify(start_end_tobs)





        

