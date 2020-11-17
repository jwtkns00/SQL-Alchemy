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

#Setup Flask
app = Flask(__name__)

