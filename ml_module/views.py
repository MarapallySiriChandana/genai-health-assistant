from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SymptomPrediction
import joblib
import pandas as pd
import os
from django.conf import settings

# Load model and artifacts
MODELS_DIR = os.path.join(settings.BASE_DIR, 'ml_module', 'model_files')
model = joblib.load(os.path.join(MODELS_DIR, 'disease_model.joblib'))
le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.joblib'))
symptoms_list = joblib.load(os.path.join(MODELS_DIR, 'symptoms_list.joblib'))

@login_required
def checker_view(request):
    prediction_result = None
    confidence = None
    selected_symptoms = []

    if request.method == 'POST':
        selected_symptoms = request.POST.getlist('symptoms')
        if selected_symptoms:
            # Prepare input for model
            input_data = {symptom: [0] for symptom in symptoms_list}
            for s in selected_symptoms:
                if s in input_data:
                    input_data[s] = [1]
            
            input_df = pd.DataFrame(input_data)
            
            # Predict
            pred_code = model.predict(input_df)[0]
            probs = model.predict_proba(input_df)[0]
            confidence = max(probs) * 100
            prediction_result = le.inverse_transform([pred_code])[0]
            
            # Save to DB
            SymptomPrediction.objects.create(
                user=request.user,
                symptoms=", ".join(selected_symptoms),
                predicted_disease=prediction_result,
                confidence=confidence
            )

    context = {
        'symptoms_list': symptoms_list,
        'prediction': prediction_result,
        'confidence': confidence,
        'selected_symptoms': selected_symptoms
    }
    return render(request, 'ml_module/checker.html', context)
