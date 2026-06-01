import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Create a small real-world-like dataset
data = {
    'sneezing': [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'sore_throat': [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'runny_nose': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'cough': [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    'fever': [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    'body_ache': [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0],
    'headache': [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    'tiredness': [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    'loss_of_taste': [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    'difficulty_breathing': [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
    'chills': [0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0],
    'sweating': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    'nausea': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    'excessive_thirst': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    'frequent_urination': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    'blurred_vision': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    'disease': [
        'Common Cold', 'Common Cold', 'Flu', 'Flu', 'Covid-19', 'Covid-19', 
        'Malaria', 'Malaria', 'Common Cold', 'Covid-19', 'Pneumonia', 'Diabetes'
    ]
}

df = pd.DataFrame(data)

# Features and Target
X = df.drop('disease', axis=1)
y = df['disease']

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# Save model and artifacts
model_dir = 'ml_module/model_files'
os.makedirs(model_dir, exist_ok=True)

joblib.dump(model, os.path.join(model_dir, 'disease_model.joblib'))
joblib.dump(le, os.path.join(model_dir, 'label_encoder.joblib'))
joblib.dump(list(X.columns), os.path.join(model_dir, 'symptoms_list.joblib'))

print("ML Model trained and saved successfully.")
print("Symptoms:", list(X.columns))
