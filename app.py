from flask import Flask, render_template, request, jsonify
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

def get_closing_prices(data):
    closing_prices = []
    for date, values in data.items():
        closing_prices.append(float(values['4. close']))
    return closing_prices

def predict_closing_prices(X_train, y_train, X_test):
    model = LinearRegression()
    model.fit(np.array(X_train).reshape(-1, 1), y_train)
    y_pred = model.predict(np.array(X_test).reshape(-1, 1))
    return y_pred

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    symbol = request.form.get("symbol")
    api_key = "AAPL"  # Replace with your actual API key

    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",
        "datatype": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()["Time Series (Daily)"]

    dates = list(data.keys())
    actual_closing_prices = get_closing_prices(data)
    
    X_train = list(range(len(actual_closing_prices)))
    y_train = actual_closing_prices
    X_test = list(range(len(actual_closing_prices), len(actual_closing_prices) + 5))
    predicted_closing_prices = predict_closing_prices(X_train, y_train, X_test)

    return jsonify({
        "dates": dates,
        "actual_closing_prices": actual_closing_prices,
        "predicted_closing_prices": predicted_closing_prices.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
