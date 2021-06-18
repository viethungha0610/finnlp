"""
API End-point codes
"""

from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS
import getdata
import nlputils
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

"""
High level idea:
    - This API will response with json data, meant to serve the React front-end
"""

# Pandas DataFrame containing news headline data
# Class initiation
nlp_app_instance = getdata.NlpApp()

@app.route("/sentiments")
def return_sentiments():
    nlp_app_instance.collect_data()
    nlp_app_instance.evaluate_sentiment()
    sentiment_dict = dict(pd.Series(nlp_app_instance.latest_sentiment_list_).value_counts())
    # Avoiding type error
    for k, v in sentiment_dict.items():
        sentiment_dict[k] = int(v)
    return jsonify(sentiment_dict)

@app.route("/datatable")
def return_data_table():
    try:
        return jsonify(json.loads(nlp_app_instance.latest_data_evaluated_.to_json(orient="records")))
    except AttributeError: # If data is not collected -> There will be an Attribute error
        nlp_app_instance.collect_data()
        nlp_app_instance.evaluate_sentiment()
        return jsonify(json.loads(nlp_app_instance.latest_data_evaluated_.to_json(orient="records")))

@app.route("/refresh")
def refresh_data():
    nlp_app_instance.collect_data()
    nlp_app_instance.evaluate_sentiment()
    return "Data has been refreshed!"

@app.route("/download")
def return_data():
    return send_file("../data/newsData.xlsx",
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                    as_attachment=True)

@app.route("/topics")
def topic_modelling():
    return "This will return the topic modelling output"

@app.route("/test")
def test_sentiment():
    sentiment_dict_test = pd.read_json("../notebooks/newsSentiment.json", typ="series")
    sentiment_dict_test = dict(sentiment_dict_test)
    for k, v in sentiment_dict_test.items():
        sentiment_dict_test[k] = int(v)
    return jsonify(sentiment_dict_test)

@app.route("/testdata")
def test_data():
    with open('./testTable.json') as file:
        data_table = json.load(file)
    return jsonify(data_table)

if __name__ == "__main__":
    app.run()