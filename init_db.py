import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_health_assistant.settings')
import django
django.setup()

from django.contrib.auth.models import User
from drugs.models import DrugInfo
from accounts.models import Profile

def initialize():
    # Create Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        Profile.objects.get_or_create(user=admin, full_name="System Administrator")
        print("Admin user created: admin / admin123")
    else:
        print("Admin user already exists.")

    # Create Sample Drugs
    drugs = [
        {"name": "Paracetamol", "usage": "Pain relief, headache, fever, cold symptoms", "side_effects": "Nausea, allergic reactions, liver damage if overdosed", "dosage": "500mg-1000mg every 4-6 hours, max 4g per day"},
        {"name": "Albuterol", "usage": "Asthma, COPD, shortness of breath relief, bronchospasm", "side_effects": "Headache, tremors, palpitations, nervousness", "dosage": "90mcg inhaler, 2 puffs every 4-6 hours as needed, or 2-4mg oral tablets"},
        {"name": "Fluticasone", "usage": "Asthma prevention, chronic asthma management, inhaled corticosteroid", "side_effects": "Hoarseness, throat irritation, oral candidiasis", "dosage": "110-220mcg inhaler, 2 puffs twice daily"},
        {"name": "Leukotrienes Inhibitor", "usage": "Asthma control, allergy-induced asthma, exercise-induced asthma", "side_effects": "Headache, nausea, dizziness", "dosage": "10mg once daily at bedtime"},
        {"name": "Theophylline", "usage": "Asthma, COPD, chronic bronchitis, breathing difficulty", "side_effects": "Nausea, headache, insomnia, palpitations", "dosage": "300-400mg daily in divided doses"},
        {"name": "Ibuprofen", "usage": "Pain relief, inflammation, fever, arthritis, menstrual cramps", "side_effects": "Stomach upset, heartburn, dizziness", "dosage": "200mg-400mg every 4-6 hours, max 1200mg daily"},
        {"name": "Aspirin", "usage": "Pain relief, fever, heart attack prevention, blood clotting prevention", "side_effects": "Stomach irritation, bleeding, allergic reactions", "dosage": "325mg-500mg every 4-6 hours"},
        {"name": "Amoxicillin", "usage": "Bacterial infections, ear infection, strep throat, pneumonia", "side_effects": "Diarrhea, nausea, rash, allergic reactions", "dosage": "250mg-500mg 3 times a day for 7-10 days"},
        {"name": "Azithromycin", "usage": "Bacterial infections, respiratory infections, strep throat", "side_effects": "Diarrhea, nausea, abdominal pain", "dosage": "500mg on day 1, then 250mg daily for 4 days"},
        {"name": "Cephalexin", "usage": "Bacterial skin infections, urinary tract infections, respiratory infections", "side_effects": "Diarrhea, nausea, allergic reactions", "dosage": "250mg-500mg every 6 hours"},
        {"name": "Metformin", "usage": "Type 2 Diabetes, blood sugar control, weight management", "side_effects": "Stomach upset, metallic taste, diarrhea, vitamin B12 deficiency", "dosage": "500mg once or twice daily, up to 2550mg daily"},
        {"name": "Insulin", "usage": "Type 1 Diabetes, Type 2 Diabetes, high blood sugar", "side_effects": "Low blood sugar, weight gain, injection site reactions", "dosage": "Variable based on blood glucose levels"},
        {"name": "Atorvastatin", "usage": "High cholesterol, heart disease prevention, cardiovascular health", "side_effects": "Muscle pain, digestive problems, liver enzyme changes", "dosage": "10mg-80mg once daily"},
        {"name": "Lisinopril", "usage": "High blood pressure, heart failure, heart attack prevention", "side_effects": "Dizziness, cough, fatigue, hyperkalemia", "dosage": "10mg once daily initially"},
        {"name": "Metoprolol", "usage": "High blood pressure, angina, heart failure, migraine prevention", "side_effects": "Fatigue, dizziness, cold hands/feet, slow heart rate", "dosage": "25mg-100mg once or twice daily"},
        {"name": "Omeprazole", "usage": "Acid reflux, GERD, peptic ulcers, heartburn", "side_effects": "Headache, nausea, diarrhea or constipation", "dosage": "20mg-40mg once daily for 14-28 days"},
        {"name": "Ranitidine", "usage": "Acid reflux, heartburn, ulcers, GERD", "side_effects": "Headache, dizziness, diarrhea", "dosage": "150mg twice daily or 300mg once daily"},
        {"name": "Loratadine", "usage": "Allergies, hay fever, itching, hives, allergic rhinitis", "side_effects": "Headache, dry mouth, drowsiness (minimal)", "dosage": "10mg once daily"},
        {"name": "Cetirizine", "usage": "Allergies, allergy symptoms, hay fever, hives, itching", "side_effects": "Drowsiness, dry mouth, fatigue", "dosage": "5mg-10mg once daily"},
        {"name": "Diphenhydramine", "usage": "Allergies, antihistamine, sleep aid, motion sickness", "side_effects": "Drowsiness, dry mouth, dizziness, blurred vision", "dosage": "25mg-50mg every 4-6 hours as needed"},
        {"name": "Sertraline", "usage": "Depression, anxiety, panic disorder, OCD, PTSD", "side_effects": "Nausea, headache, sexual dysfunction, insomnia", "dosage": "50mg once daily, up to 200mg daily"},
        {"name": "Fluoxetine", "usage": "Depression, anxiety, OCD, eating disorders, panic disorder", "side_effects": "Nausea, insomnia, headache, dry mouth", "dosage": "20mg once daily, up to 80mg daily"},
        {"name": "Amitriptyline", "usage": "Depression, chronic pain, migraine prevention, nerve pain", "side_effects": "Drowsiness, dry mouth, weight gain, constipation", "dosage": "25mg-75mg at bedtime"},
        {"name": "Gabapentin", "usage": "Nerve pain, neuropathy, seizures, restless leg syndrome", "side_effects": "Drowsiness, dizziness, coordination problems", "dosage": "300mg-600mg three times daily"},
        {"name": "Tramadol", "usage": "Moderate pain relief, postoperative pain, chronic pain", "side_effects": "Dizziness, nausea, constipation, seizure risk", "dosage": "50mg-100mg every 4-6 hours, max 400mg daily"},
        {"name": "Codeine", "usage": "Cough suppression, pain relief, mild to moderate pain", "side_effects": "Drowsiness, constipation, dizziness, nausea", "dosage": "10mg-20mg every 4-6 hours for cough"},
        {"name": "Dextromethorphan", "usage": "Cough suppression, dry cough relief", "side_effects": "Drowsiness, dizziness, nausea", "dosage": "10mg-20mg every 4 hours, or 30mg every 6-8 hours"},
        {"name": "Guaifenesin", "usage": "Expectorant, productive cough relief, mucus clearance", "side_effects": "Nausea, vomiting, dizziness, headache", "dosage": "200mg-400mg every 4 hours, up to 2400mg daily"},
        {"name": "Phenylephrine", "usage": "Nasal congestion, decongestant, sinus pressure relief", "side_effects": "Nervousness, headache, insomnia, increased heart rate", "dosage": "10mg every 4 hours, max 60mg daily"},
        {"name": "Pseudoephedrine", "usage": "Nasal congestion, decongestant, sinus relief", "side_effects": "Nervousness, insomnia, increased heart rate, anxiety", "dosage": "30mg-60mg every 4-6 hours, max 240mg daily"},
        {"name": "Acetaminophen", "usage": "Pain relief, fever, headache, muscle aches, cold symptoms", "side_effects": "Rare, liver damage if overdosed, allergic reactions", "dosage": "325mg-650mg every 4-6 hours, max 4g daily"},
        {"name": "Montelukast", "usage": "Asthma, allergy-induced asthma, allergic rhinitis", "side_effects": "Headache, nausea, behavior changes in children", "dosage": "4-10mg once daily in evening"},
        {"name": "Dengue Treatment - Acetaminophen", "usage": "Dengue fever pain and fever relief", "side_effects": "Liver damage at high doses, allergic reactions", "dosage": "500-1000mg every 4-6 hours, avoid aspirin and NSAIDs"},
        {"name": "IV Fluid Therapy", "usage": "Dengue fever, severe dehydration, hypovolemic shock", "side_effects": "Rare - fluid overload, electrolyte imbalance", "dosage": "1-2L IV saline per day based on clinical assessment"},
        {"name": "Platelet Transfusion", "usage": "Dengue hemorrhagic fever, thrombocytopenia, bleeding risk", "side_effects": "Rare - transfusion reaction, alloimmunization", "dosage": "1 unit of platelet concentrate when count <20,000/μL"},
        {"name": "Fresh Frozen Plasma", "usage": "Dengue hemorrhagic fever, coagulopathy management", "side_effects": "Fever, chills, allergic reactions, circulatory overload", "dosage": "10-15 mL/kg IV, repeat based on PT/INR improvement"},
        {"name": "Dextran", "usage": "Dengue shock syndrome, plasma volume expansion, colloid therapy", "side_effects": "Allergic reactions, acute kidney injury, bleeding", "dosage": "500mL-1000mL IV, max 20mL/kg/day"},
    ]

    for drug in drugs:
        DrugInfo.objects.get_or_create(**drug)
    print("Sample drug data initialized.")

if __name__ == "__main__":
    initialize()
