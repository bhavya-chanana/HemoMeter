import pickle
import pandas as pd
import os

def predict_hb(data):
    '''
    predicted_hb 
    param data -> dict with features, Age, Gender, video_name
    return prediction -> predicted Hb value
    '''
    # Load the trained SVR model from the pickle file
    model_path = os.path.join('models', 'svr_model.pkl')
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    # Define the expected features
    features = ['Tu/Tpi', 'Tv/Tpi', 'Tw/Tpi', 'Tu', 'Tv', 'Tw', 'Asp', 'Adn', 'Adp', 'Tpi', 'Tsp', 'Tsys', 'Tdp', 'deltaT', 'Tsp/Tpi', 'Age', 'Gender']

    data_df = pd.DataFrame([data])

    prediction = model.predict(data_df[features])

    return prediction[0]

