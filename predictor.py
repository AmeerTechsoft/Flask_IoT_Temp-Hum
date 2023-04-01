# Declearing Libraries

import pandas as pd
import matplotlib.pyplot as plt
from autots import AutoTS
from autots.datasets import load_daily
import pytz


CHANNEL_ID = 2039086

# Load data from ThingSpeak channel as .CSV into dataframe
data = pd.read_csv(f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?&results=2000')

# Shows what the dataframe contains

# converting Field1 and Field2 to Float string type

data['field1'] = pd.to_numeric(data['field1'], errors='coerce').astype(float)

data['field2'] = pd.to_numeric(data['field2'], errors='coerce').astype(float)

data.dropna(inplace=True)

timezone_wca = pytz.timezone('Africa/Lagos')


# Convert timestamp to datetime format
data['created_at'] = pd.to_datetime(data['created_at']).dt.tz_convert(timezone_wca)

# Set timestamp as index
data.set_index('created_at', inplace=True)
data_hourly = data.resample("H").mean().fillna(method="ffill")

# Select temperature data and humidity data from dataframe
temp_data = data_hourly['field1']
hum_data = data_hourly['field2']

# model for temp
temp_model = AutoTS(
    forecast_length=6,  # Forecasting every 4 hours for a day, so 6 forecasts
    frequency='4H',
    prediction_interval=0.7,
    ensemble='simple',
    model_list='multivariate',
    transformer_list='superfast',
    drop_most_recent=1,
    max_generations=5,
    num_validations=1,
    models_to_validate=0.2,
    n_jobs=100,
)


# model for humidity
hum_model = AutoTS(
    forecast_length=6,  # Forecasting every 4 hours for a day, so 6 forecasts
    frequency='4H',
    prediction_interval=0.7,
    ensemble='simple',
    model_list='multivariate',
    transformer_list='superfast',
    drop_most_recent=1,
    max_generations=5,
    num_validations=1,
    models_to_validate=0.2,
    n_jobs=100,

)

temp_model.fit(temp_data)
temp_forecast = temp_model.predict().forecast

hum_model.fit(hum_data)
hum_forecast = hum_model.predict().forecast

# Combine the predictions into a single DataFrame
preds = pd.merge(temp_forecast, hum_forecast, left_index=True, right_index=True)


# Export the predictions to a CSV file
preds.to_csv('predicted/predictions.csv')

