import os

import numpy as np
import pandas as pd
import pickle
import threading

from database import risk_database

__currently_loaded_model = None
__is_model_loaded = False


def load_model(model_path="fluprint_ai_model.pkl"):
    global __currently_loaded_model, __is_model_loaded

    if __is_model_loaded:
        return __currently_loaded_model

    current_dir = os.path.dirname(__file__)

    model_full_path = os.path.join(current_dir, model_path)

    with open(model_full_path, "rb") as f:
        model = pickle.load(f)

    __currently_loaded_model = model
    __is_model_loaded = True

    return model


def compute_risk_from_data(data):
    model = load_model()

    data_df = pd.DataFrame([data])

    expected_features = model.get_booster().feature_names

    for col in data_df.select_dtypes(include=['object']).columns:
        data_df[col] = data_df[col].astype('category')

    for col in data_df.select_dtypes(include=['category']).columns:
        data_df[col] = data_df[col].cat.codes

    missing_features = set(expected_features) - set(data_df.columns)
    missing_df = pd.DataFrame({feature: [np.nan] * len(data_df) for feature in missing_features})

    data_df = pd.concat([data_df, missing_df], axis=1)

    data_df = data_df[expected_features]

    prediction = model.predict(data_df)

    return prediction[0] == 1


def compute_risk(id: int, data: dict) -> bool:
    print("TID #" + str(threading.get_ident()), 
          "Computing risk for", "id:", id, ", data:", data)
    
    at_risk = compute_risk_from_data(data)
    
    print("TID #" + str(threading.get_ident()), 
          "Completed risk computation!", "id:", id, ", at_risk:", at_risk)
    
    print("TID #" + str(threading.get_ident()), "Writing to database...")
    risk_database.end(id, at_risk)
    print("TID #" + str(threading.get_ident()), "OK")

    return at_risk
