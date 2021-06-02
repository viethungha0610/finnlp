from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS
import getdata
import nlputils
import pandas as pd

app = Flask(__name__)
CORS(app)

"""
High level idea:
    - This API will response with json data, meant to serve the React front-end
"""

news_data = getdata.collect_data()

@app.route("/sentiments")
def return_sentiments():
    sentiment_list = nlputils.extract_sentiment(news_data)
    sentiment_dict = dict(pd.Series(sentiment_list).value_counts())
    for k, v in sentiment_dict.items():
        sentiment_dict[k] = int(v)
    return sentiment_dict

@app.route("/data")
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

if __name__ == "__main__":
    app.run()