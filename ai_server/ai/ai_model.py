import os

import numpy as np
import pandas as pd

from database import risk_database
import pickle

def load_model(model_path="fluprint_ai_model.pkl"):
    current_dir = os.path.dirname(__file__)

    model_full_path = os.path.join(current_dir, model_path)

    with open(model_full_path, "rb") as f:
        model = pickle.load(f)

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
    at_risk = compute_risk_from_data(data)

    risk_database.end(id, at_risk)

    return at_risk
