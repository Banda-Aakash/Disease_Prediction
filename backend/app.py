import numpy as np
import pandas as pd
from statistics import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "Training.csv")
TEST_DATA_PATH = os.path.join(BASE_DIR, "dataset", "Testing.csv")

# Load and preprocess data
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# Prepare the symptoms list
symptoms = data.columns.tolist()

encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Train models on whole data
final_svm_model = SVC(probability=True)
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
final_svm_model.fit(X, y)
final_nb_model.fit(X, y)
final_rf_model.fit(X, y)

symptoms = X.columns.values
symptom_index = {value: idx for idx, value in enumerate(symptoms)}

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}

# Prediction function
def predictDisease(symptoms):
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"].get(symptom, None)
        if index is not None:
            input_data[index] = 1
    
    input_data = np.array(input_data).reshape(1, -1)
    input_df = pd.DataFrame(input_data, columns=X.columns)

    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_df)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_df)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_df)[0]]
    
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }
    return predictions

# Flask endpoint for predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('selectedSymptoms', [])
    predictions = predictDisease(symptoms)
    return jsonify(predictions)

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify(list(symptoms))

if __name__ == '__main__':
    app.run(debug=True)
