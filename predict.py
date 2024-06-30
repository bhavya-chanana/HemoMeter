import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import os

def predict_hb(data):
    '''
    predicted_hb 
    param data -> dict with features, Age, Gender, video_name
    return prediction -> predicted Hb value
    '''
    # Load the trained SVR model from the pickle file
    with open('D:\\Research-IIIT\\modelppg\\models\\svr_model.pkl', 'rb') as model_file:
        svr_model = pickle.load(model_file)

    # Define the expected features
    features = ['Tu/Tpi', 'Tv/Tpi', 'Tw/Tpi', 'Tu', 'Tv', 'Tw', 'Asp', 'Adn', 'Adp', 'Tpi', 'Tsp', 'Tsys', 'Tdp', 'deltaT', 'Tsp/Tpi', 'Age', 'Gender']

    data_df = pd.DataFrame([data])

    prediction = svr_model.predict(data_df[features])

    return prediction[0]

