import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'trained-model', 'decision_tree_models.pkl')

with open(model_path, 'rb') as f:
    models = pickle.load(f)

feature_columns = ['dost_exam_result', 'filipino grade', 'English grade', 'mathematics grade',
                   'science grade', 'araling panlipunan grade', 'Edukasyon sa pagpapakatao grade',
                   'Edukasyong panglipunan at pangkabuhayan grade', 'MAPEH grade', 'Average grade']

# Mapping for DOST exam result string to numeric
DOST_RESULT_MAPPING = {
    'passed': 1,
    'failed': 0,
    # add other mappings if needed
}

def predict_program_eligibility(input_data):
    # Convert dost_exam_result string to numeric if needed
    dost_result = input_data.get('dost_exam_result')
    if isinstance(dost_result, str):
        input_data['dost_exam_result'] = DOST_RESULT_MAPPING.get(dost_result.lower(), 0)

    if isinstance(input_data, dict):
        input_list = [input_data[col] for col in feature_columns]
    else:
        input_list = input_data

    df = pd.DataFrame([input_list], columns=feature_columns)

    # recommendations = {}
    # for label, model in models.items():
    #     prediction = model.predict(df)[0]
    #     recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"
    recommendations = {}
    for label, model in models.items():
        # If label is exactly "Top 5", rename it to "Top5"
        if label == "top 5":
            label = "top5"

        prediction = model.predict(df)[0]
        recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"

    return recommendations


    return recommendations
