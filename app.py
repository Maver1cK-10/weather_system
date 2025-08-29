from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Function to generate base64 graph
def get_prediction_graph(predictions):
    model_names = ['Linear Regression', 'Random Forest']
    colors = ['#74b9ff', '#00cec9']

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.bar(model_names, predictions, color=colors)
    ax.set_ylabel('Rainfall (mm)')
    ax.set_title('Rainfall Prediction by Model')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return graph_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input from form
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        pressure = float(request.form['pressure'])
        wind = float(request.form['wind'])

        # Prepare data
        df = pd.DataFrame([[temp, humidity, pressure, wind]],
                          columns=["temp", "humidity", "sealevelpressure", "windspeed"])

        # Load models
        model_path = os.path.join("models")
        scaler = joblib.load(os.path.join(model_path, "scaler.pkl"))
        logistic_model = joblib.load(os.path.join(model_path, "logistic_model.pkl"))
        linear_model = joblib.load(os.path.join(model_path, "linear_model.pkl"))
        rf_model = joblib.load(os.path.join(model_path, "random_forest_model.pkl"))

        # Preprocess and predict
        scaled = scaler.transform(df)

        is_rain = logistic_model.predict(scaled)[0]
        rain_text = "Yes, carry an umbrella!" if is_rain else "No rain expected."

        lin_pred = linear_model.predict(scaled)[0]
        rf_pred = rf_model.predict(df)[0]
        cloud_cover = "Overcast" if is_rain else "Clear"

        # Generate graph as base64
        graph_img = get_prediction_graph([lin_pred, rf_pred])

        return render_template("predict.html",
                               rain_text=rain_text,
                               lin_pred=f"{lin_pred:.2f}",
                               rf_pred=f"{rf_pred:.2f}",
                               cloud_cover=cloud_cover,
                               graph_img=graph_img)
    except Exception as e:
        return f"<h3>Error:</h3><pre>{str(e)}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
