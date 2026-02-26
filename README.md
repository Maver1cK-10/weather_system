Fake News Detection Web App
Overview

This project is a machine learning-based fake news detection web application built using:

Flask (Web framework)

Scikit-learn (ML models)

Joblib (Model persistence)

The application allows users to input news text and receive:

Individual predictions from multiple ML models

A final prediction from the default model

Model accuracy comparisons

Features

Text preprocessing (URL removal, normalization, punctuation cleaning)

TF-IDF vectorization

Multiple classification models:

Logistic Regression

Random Forest

Naive Bayes

Model comparison display

Clean web interface using Flask templates

Project Structure
FakeNewsDetection/
│
├── app.py
├── requirements.txt
├── models/
│   ├── vectorizer.pkl
│   ├── model.pkl
│   ├── logistic_model.pkl
│   ├── random_forest.pkl
│   └── naive_bayes.pkl
│
├── templates/
│   └── result.html
│
└── README.md
Installation
1️) Clone the repository
git clone https://github.com/yourusername/fake-news-detector.git
cd fake-news-detector
2️) Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
3️) Install dependencies
pip install -r requirements.txt
Running the Application
python app.py

Flask will start at:

http://127.0.0.1:5000/
How It Works
1. Text Cleaning

Converts text to lowercase

Removes URLs

Removes special characters

Normalizes whitespace

2. Vectorization

Uses a pre-trained TF-IDF vectorizer:

vectorizer.transform([cleaned_text])
3. Prediction

Each model predicts:

1 → REAL

0 → FAKE

Final output is produced by the default model.

Models Used
Model	Accuracy (%)
Logistic Regression	95.8
Random Forest	94.2
Naive Bayes	90.5
Requirements

Python 3.9+

Pre-trained .pkl model files in models/ directory

Important Notes

The app requires all model files to exist in the models/ folder.

Model training is not included in this repository.

Accuracy values are static and manually defined.
