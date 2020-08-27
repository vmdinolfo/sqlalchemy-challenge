# 1. import libraries
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, Date, cast, distinct, desc
import datetime as dt
from datetime import timedelta

# create connection/session to db
db_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
weather = Base.classes.measurement
station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Hawaii Climate Data<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start_date/YYYY-MM-DD<br/>"
            f"/api/v1.0/date_range/YYYY-MM-DD/YYYY-MM-DD"
            )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
   
    session = Session(engine)
   
    precipitation_list = session.query(weather.date,weather.prcp).all()
    
    session.close()
   
    precipitation = []
    prcp_dict = {}
    prcp_dict = {date : prcp for date, prcp in precipitation_list}
    precipitation.append(prcp_dict)

    return jsonify(precipitation)

# 5. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'station' page...")
    
    session = Session(engine)
    
    stations = list(np.ravel(session.query(weather.station).group_by(weather.station).all()))
    
    session.close()
    
    return jsonify(stations)

# 6. Define what to do when a user hits the /about route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    session = Session(engine)

    top_station_q = session.query(weather.station).group_by(weather.station).\
                order_by(desc(func.count(weather.id))).first()
    top_station = top_station_q[0]

    # find dates for queries: most recent date, 12 months ago
    #current date
    desc_dates = session.query(weather.date).order_by(weather.date.desc()).all()

    cur_date = str(*desc_dates[0])
    cur_date_yr = int(cur_date[0 : 4])
    cur_date_mth = int(cur_date[6 : 7])
    cur_date_day = int(cur_date[8 : 10])

    # 12 months ago
    twelve_months_ago = dt.date(cur_date_yr,cur_date_mth,cur_date_day) - dt.timedelta(days=365)
    
    tobs = session.query(weather.date, weather.tobs).\
    filter(weather.station == top_station).filter(weather.date > twelve_months_ago).all()
    
    session.close()

    return jsonify(tobs)

# 6. Define what to do when a user hits the /about route
@app.route("/api/v1.0/start_date/<start_date>")
def weather_by_start_date(start_date):
    print("Server received request for 'tobs' page...")
    session = Session(engine)
    
    results = session.query(weather.date,func.min(weather.tobs),func.avg(weather.tobs)\
                ,func.max(weather.tobs)).filter(weather.date >= start_date).\
                group_by(weather.date).all()
    session.close()
    
    return jsonify(results)

    # 6. Define what to do when a user hits the /about route
@app.route("/api/v1.0/date_range/<start_date>/<end_date>")
def weather_between_start_and_end_date(start_date, end_date):
    print("Server received request for 'tobs' page...")
    session = Session(engine)
    results_range = session.query(weather.date,func.min(weather.tobs),func.avg(weather.tobs)\
            ,func.max(weather.tobs)).filter(weather.date >= start_date).\
            filter(weather.date <= end_date).group_by(weather.date).all()
    session.close()
    return jsonify(results_range)

if __name__ == "__main__":
    app.run(debug=True)
