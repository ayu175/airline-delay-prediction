#!/usr/bin/env python
# coding: utf-8

# Suppress sklearn version warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# import statements
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import numpy as np
import pickle
import datetime

# Paths configurable via env (for pipeline/parent repo); fallback to current dir for local dev
AIRPORT_ENCODINGS_PATH = os.environ.get("AIRPORT_ENCODINGS_PATH", "airport_encodings.json")
MODEL_PATH = os.environ.get("MODEL_PATH", "finalized_model.pkl")

# Import the airport encodings file
with open(AIRPORT_ENCODINGS_PATH, "r") as f:
    airports = json.load(f)

def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    create_airport_encoding is a function that creates an array the length of all arrival airports from the chosen
    departure aiport.  The array consists of all zeros except for the specified arrival airport, which is a 1.  

    Parameters
    ----------
    airport : str
        The specified arrival airport code as a string
    airports: dict
        A dictionary containing all of the arrival airport codes served from the chosen departure airport
        
    Returns
    -------
    np.array
        A NumPy array the length of the number of arrival airports.  All zeros except for a single 1 
        denoting the arrival airport.  Returns None if arrival airport is not found in the input list.
        This is a one-hot encoded airport array.

    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None

try:
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    raise RuntimeError(f"Model file '{MODEL_PATH}' not found. Set MODEL_PATH if it lives elsewhere.")

def convert_to_seconds(time_str: str) -> int:
    """
    Converts a datetime string (ISO format) to seconds since midnight.
    """
    try:
        dt = datetime.datetime.fromisoformat(time_str)
        return dt.hour * 3600 + dt.minute * 60 + dt.second
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")

# Initialize FastAPI
app = FastAPI()

#B1. return a JSON message indicating that the API is functional
@app.get("/")
def welcome():
    return {'message': "This API is functional."}

#B2. return a JSON response indicating the average departure delay in minutes
@app.get("/predict/delays")
def predict_delays(
    DEST_AIRPORT: str = Query(..., description="Arrival airport code"),
    DEPARTURE_TIME: str = Query(..., description="Local departure time in ISO format (e.g., 2024-08-15T14:00:00)"),
    ARRIVAL_TIME: str = Query(..., description="Local arrival time in ISO format (e.g., 2024-08-15T17:00:00)")
):
    # One-hot encode the airport
    airport_encoding = create_airport_encoding(DEST_AIRPORT, airports)
    if airport_encoding is None:
        raise HTTPException(status_code=404, detail="Arrival airport not found in encodings.")

    # Convert times to seconds since midnight
    dep_seconds = convert_to_seconds(DEPARTURE_TIME)
    arr_seconds = convert_to_seconds(ARRIVAL_TIME)

    # Construct feature array
    poly_order = 1
    features = np.concatenate(([poly_order], airport_encoding, [dep_seconds, arr_seconds])).reshape(1, -1)

    # Make prediction
    try:
        prediction = model.predict(features)
        delay_minutes = float(prediction.item())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return JSONResponse(content={"average_departure_delay_minutes": delay_minutes})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("delay_prediction_api:app", host="0.0.0.0", port=8000, reload=True)
