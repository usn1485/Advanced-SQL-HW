import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# sqlite:///Resources/hawaii.sqlite

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/<start> </br>"
        f"/api/v1.0/<start>/<end> </br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
   

     session=Session(engine)
     results= session.query(Measurement.date,Measurement.prcp).all()
     session.close()
    # # Create a dictionary from the row data and append to a list of all_passengers
    
     measurment_dict=dict(results)
     return(jsonify(measurment_dict))
    
# Return a JSON list of stations from the dataset

@app.route("/api/v1.0/stations")    
def stations():
    #Query All Stations
    session=Session(engine)
    results= session.query(Measurement.station).distinct().all()
    session.close()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return (jsonify(all_stations))

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').all()
    session.close()
    all_tobs=[]
    for tob in results:
        all_tobs.append(tob[1])

    return (jsonify(all_tobs))


@app.route("/api/v1.0/<start>")
def tempstat(start):
    session=Session(engine)
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    return(jsonify(list(np.ravel(results))))

@app.route("/api/v1.0/<start>/<end>")
def tempstat_start_end_date(start,end):
    session=Session(engine)
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return(jsonify(list(np.ravel(results))))

if __name__ == '__main__':
    app.run(debug=True)
