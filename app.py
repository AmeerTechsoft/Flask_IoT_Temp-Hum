# import pandas as pd
# import json
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/chart_data')
# def chart_data():
#     # Load the predicted data from the CSV file
#     preds = pd.read_csv('predicted/predictions.csv', index_col=0, parse_dates=True)
#
#     # Select temperature data and humidity data from dataframe
#     temp_data = preds['field1']
#     hum_data = preds['field2']
#
#     # extract datetime from index
#     datetime_index = temp_data.index
#     datetime_labels = datetime_index.strftime('%Y-%m-%d %H:%M:%S').tolist()
#
#     # create a dictionary with the chart data
#     chart_data = {
#         'labels': datetime_labels,
#         'datasets': [{
#             'label': 'Temperature',
#             'data': temp_data.values.tolist(),
#             'fill': False,
#             'borderColor': 'rgb(75, 192, 192)',
#             'lineTension': 0.1
#         }, {
#             'label': 'Humidity',
#             'data': hum_data.values.tolist(),
#             'fill': False,
#             'borderColor': 'rgb(255, 99, 132)',
#             'lineTension': 0.1
#         }]
#     }
#
#     # convert the chart data to JSON
#     chart_data_json = json.dumps(chart_data)
#
#     # return the chart data as JSON
#     return chart_data_json
#
#
# if __name__ == '__main__':
#     app.run()

import sqlite3
import pandas as pd
import json
from flask import Flask, render_template
import requests


app = Flask(__name__)

# connect to the database
conn = sqlite3.connect('predicted_data.db')
c = conn.cursor()
# create a table to store the chart data
c.execute('''CREATE TABLE IF NOT EXISTS predicted_data
             (datetime text, temperature real, humidity real)''')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thingspeak_feed')
def thingspeak_feed():
    channel_id = '2039086'
    api_key = 'LXOTOE6HKVWNHZ63'
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data


@app.route('/chart_data')
def chart_data():
    # Load the predicted data from the CSV file
    prediction = pd.read_csv('predicted/predictions.csv', index_col=0, parse_dates=True)

    # Select temperature data and humidity data from dataframe
    temp_data = prediction['field1']
    hum_data = prediction['field2']

    # extract datetime from index
    datetime_index = temp_data.index
    datetime_labels = datetime_index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    with sqlite3.connect('predicted_data.db') as conn:
        for i, row in prediction.iterrows():
            conn.execute("INSERT INTO predicted_data (datetime, temperature, humidity) VALUES (?, ?, ?)",
                             (i.to_pydatetime(), row['field1'], row['field2']))
        conn.commit()
        print("Data inserted successfully.")


    # create a dictionary with the chart data
    chart_data = {
        'labels': datetime_labels,
        'datasets': [{
            'label': 'Temperature',
            'data': temp_data.values.tolist(),
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'lineTension': 0.1
        }, {
            'label': 'Humidity',
            'data': hum_data.values.tolist(),
            'fill': False,
            'borderColor': 'rgb(255, 99, 132)',
            'lineTension': 0.1
        }]
    }

    # convert the chart data to JSON
    chart_data_json = json.dumps(chart_data)

    # return the chart data as JSON
    return chart_data_json


if __name__ == '__main__':
    app.run()
