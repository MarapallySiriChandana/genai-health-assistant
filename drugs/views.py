from django.shortcuts import render
from .models import DrugInfo
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_drug_info_from_gemini(query):
    """Fetch REAL comprehensive drug information from Gemini API - GUARANTEED results"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # ULTRA-EXPLICIT prompt that demands real drugs ONLY
        prompt = f"""You are a pharmaceutical database. Return exactly 4 REAL drugs for: "{query}"

RETURN FORMAT (exactly as shown):
1. Acetaminophen|Used for fever and pain|Rare side effects, liver damage if overdosed|500-1000mg every 4-6 hours
2. Ibuprofen|Used for inflammation and fever|Stomach upset, heartburn|200-400mg every 4-6 hours
3. [Drug3]|[Usage]|[Side Effects]|[Dosage]
4. [Drug4]|[Usage]|[Side Effects]|[Dosage]

RULES - DO NOT VIOLATE:
- Use | (pipe) as separator ONLY
- Each line starts with number like: 1. 2. 3. 4.
- REAL drug names only
- NEVER use generic text like "Treatment", "Information", "Options"
- If "{query}" is dengue: return Acetaminophen, IV Fluids, Paracetamol, Platelet products
- If "{query}" is asthma: return Albuterol, Fluticasone, Montelukast, Theophylline
- If "{query}" is diabetes: return Metformin, Insulin, Glipizide, Linagliptin
- For any health term: return REAL drugs, not descriptions"""
        
        response = model.generate_content(prompt, timeout=15)
        text = response.text.strip()
        
        print(f"\n{'='*70}")
        print(f"GEMINI RESPONSE FOR: {query}")
        print(f"{'='*70}")
        print(text)
        print(f"{'='*70}\n")
        
        drugs = []
        
        # Parse the pipe-separated format
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line or '|' not in line:
                continue
            
            # Split by pipe
            parts = line.split('|')
            if len(parts) >= 4:
                # Remove numbering and clean name
                name = parts[0].strip()
                # Remove "1.", "2." etc prefix
                if name and name[0].isdigit() and '.' in name[:3]:
                    name = name.split('.', 1)[1].strip()
                
                usage = parts[1].strip()
                effects = parts[2].strip()
                dosage = parts[3].strip()
                
                # Validate it's not generic
                if name and 'treatment' not in name.lower() and 'information' not in name.lower() and 'varies' not in name.lower():
                    drug = {
                        'name': name,
                        'usage': usage if usage else f'Treatment for {query}',
                        'side_effects': effects if effects else 'Consult healthcare provider',
                        'dosage': dosage if dosage else 'As prescribed'
                    }
                    if drug not in drugs:  # Avoid duplicates
                        drugs.append(drug)
        
        if len(drugs) >= 3:
            print(f"✓ SUCCESS: Extracted {len(drugs)} REAL drugs from Gemini\n")
            return drugs[:4]
        
        print(f"⚠ Pipe format parsing got {len(drugs)} drugs, trying line-by-line...\n")
        
        # Fallback: Extract any drug data from response
        drugs = []
        for line in lines:
            if not line.strip():
                continue
            
            # Look for numbered lines with data
            if line[0].isdigit() and '.' in line[:3]:
                line = line.split('.', 1)[1].strip()
            
            # If it has pipe separators, parse it
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    drug = {
                        'name': parts[0],
                        'usage': parts[1] if len(parts) > 1 else f'Treatment for {query}',
                        'side_effects': parts[2] if len(parts) > 2 else 'Consult provider',
                        'dosage': parts[3] if len(parts) > 3 else 'As prescribed'
                    }
                    if drug['name'] and 'treatment' not in drug['name'].lower():
                        drugs.append(drug)
        
        if drugs:
            print(f"✓ Fallback extracted {len(drugs)} drugs\n")
            return drugs[:4]
        
        print(f"✗ Failed to extract real drugs from Gemini\n")
        return []
        
    except Exception as e:
        print(f"✗ Gemini API Error: {e}\n")
        return []


# HARDCODED DRUG DATA BY CONDITION (Ultimate Fallback)
COMMON_DRUGS_DB = {
    'default': [
        {'name': 'Acetaminophen', 'usage': 'Pain relief, fever, headache', 'side_effects': 'Rare, liver damage if overdosed', 'dosage': '500-1000mg every 4-6 hours'},
        {'name': 'Ibuprofen', 'usage': 'Pain, inflammation, fever', 'side_effects': 'Stomach upset, heartburn', 'dosage': '200-400mg every 4-6 hours'},
        {'name': 'Aspirin', 'usage': 'Pain relief, heart protection', 'side_effects': 'Stomach irritation, bleeding', 'dosage': '325-500mg every 4-6 hours'},
    ],
    'dengue': [
        {'name': 'Acetaminophen', 'usage': 'Dengue fever pain and fever relief', 'side_effects': 'Liver damage at high doses', 'dosage': '500-1000mg every 4-6 hours'},
        {'name': 'IV Fluid Therapy', 'usage': 'Dengue fever, severe dehydration, hypovolemic shock', 'side_effects': 'Fluid overload, electrolyte imbalance', 'dosage': '1-2L IV saline per day'},
        {'name': 'Platelet Transfusion', 'usage': 'Dengue hemorrhagic fever, thrombocytopenia', 'side_effects': 'Transfusion reaction, alloimmunization', 'dosage': '1 unit when count <20,000/μL'},
    ],
    'asthma': [
        {'name': 'Albuterol', 'usage': 'Asthma, COPD, shortness of breath, bronchospasm', 'side_effects': 'Headache, tremors, palpitations', 'dosage': '90mcg inhaler, 2 puffs every 4-6 hours'},
        {'name': 'Fluticasone', 'usage': 'Asthma prevention, chronic asthma management', 'side_effects': 'Hoarseness, throat irritation, oral candidiasis', 'dosage': '110-220mcg inhaler, twice daily'},
        {'name': 'Montelukast', 'usage': 'Asthma control, allergy-induced asthma, exercise-induced', 'side_effects': 'Headache, nausea, behavior changes', 'dosage': '4-10mg once daily in evening'},
    ],
    'diabetes': [
        {'name': 'Metformin', 'usage': 'Type 2 Diabetes, blood sugar control, weight management', 'side_effects': 'Stomach upset, metallic taste, diarrhea', 'dosage': '500-1500mg daily in divided doses'},
        {'name': 'Insulin', 'usage': 'Type 1 & 2 Diabetes, high blood sugar', 'side_effects': 'Low blood sugar, weight gain, injection pain', 'dosage': 'Variable based on blood glucose levels'},
        {'name': 'Glipizide', 'usage': 'Type 2 Diabetes, stimulate insulin release', 'side_effects': 'Hypoglycemia, weight gain, dizziness', 'dosage': '5-10mg daily before meals'},
    ],
    'heart': [
        {'name': 'Atorvastatin', 'usage': 'High cholesterol, heart disease prevention', 'side_effects': 'Muscle pain, liver enzyme changes', 'dosage': '10mg-80mg once daily'},
        {'name': 'Lisinopril', 'usage': 'High blood pressure, heart failure, heart protection', 'side_effects': 'Dizziness, cough, fatigue', 'dosage': '10mg once daily initially'},
        {'name': 'Metoprolol', 'usage': 'High blood pressure, angina, heart failure', 'side_effects': 'Fatigue, dizziness, slow heart rate', 'dosage': '25mg-100mg once or twice daily'},
    ],
    'allergy': [
        {'name': 'Loratadine', 'usage': 'Allergies, hay fever, itching, hives, allergic rhinitis', 'side_effects': 'Headache, dry mouth, minimal drowsiness', 'dosage': '10mg once daily'},
        {'name': 'Cetirizine', 'usage': 'Allergies, allergy symptoms, urticaria, hay fever', 'side_effects': 'Drowsiness, dry mouth, fatigue', 'dosage': '5mg-10mg once daily'},
        {'name': 'Diphenhydramine', 'usage': 'Allergies, antihistamine, sleep aid', 'side_effects': 'Drowsiness, dry mouth, dizziness', 'dosage': '25mg-50mg every 4-6 hours'},
    ],
    'depression': [
        {'name': 'Sertraline', 'usage': 'Depression, anxiety, panic disorder, OCD, PTSD', 'side_effects': 'Nausea, headache, sexual dysfunction, insomnia', 'dosage': '50mg once daily, up to 200mg daily'},
        {'name': 'Fluoxetine', 'usage': 'Depression, anxiety, OCD, eating disorders', 'side_effects': 'Nausea, insomnia, headache, dry mouth', 'dosage': '20mg once daily, up to 80mg daily'},
        {'name': 'Amitriptyline', 'usage': 'Depression, chronic pain, migraine prevention', 'side_effects': 'Drowsiness, dry mouth, weight gain', 'dosage': '25mg-75mg at bedtime'},
    ],
    'cough': [
        {'name': 'Dextromethorphan', 'usage': 'Cough suppression, dry cough relief', 'side_effects': 'Drowsiness, dizziness, nausea', 'dosage': '10mg-20mg every 4 hours'},
        {'name': 'Codeine', 'usage': 'Cough suppression, pain relief', 'side_effects': 'Drowsiness, constipation, dizziness', 'dosage': '10mg-20mg every 4-6 hours'},
        {'name': 'Guaifenesin', 'usage': 'Expectorant, productive cough relief, mucus clearance', 'side_effects': 'Nausea, vomiting, dizziness', 'dosage': '200-400mg every 4 hours'},
    ],
    'infection': [
        {'name': 'Amoxicillin', 'usage': 'Bacterial infections, ear infection, pneumonia', 'side_effects': 'Diarrhea, nausea, rash, allergic reactions', 'dosage': '250mg-500mg 3 times daily for 7-10 days'},
        {'name': 'Azithromycin', 'usage': 'Bacterial infections, respiratory infections', 'side_effects': 'Diarrhea, nausea, abdominal pain', 'dosage': '500mg day 1, then 250mg daily for 4 days'},
        {'name': 'Cephalexin', 'usage': 'Bacterial skin infections, UTI, respiratory', 'side_effects': 'Diarrhea, nausea, allergic reactions', 'dosage': '250mg-500mg every 6 hours'},
    ],
    'acid_reflux': [
        {'name': 'Omeprazole', 'usage': 'Acid reflux, GERD, peptic ulcers, heartburn', 'side_effects': 'Headache, nausea, diarrhea or constipation', 'dosage': '20mg-40mg once daily for 14-28 days'},
        {'name': 'Ranitidine', 'usage': 'Acid reflux, heartburn, ulcers, GERD', 'side_effects': 'Headache, dizziness, diarrhea', 'dosage': '150mg twice daily or 300mg once daily'},
        {'name': 'Antacid', 'usage': 'Heartburn relief, acid reflux, indigestion', 'side_effects': 'Constipation or diarrhea, nausea', 'dosage': 'As needed after meals'},
    ],
    'pain': [
        {'name': 'Tramadol', 'usage': 'Moderate pain relief, postoperative pain', 'side_effects': 'Dizziness, nausea, constipation, seizure risk', 'dosage': '50mg-100mg every 4-6 hours, max 400mg/day'},
        {'name': 'Gabapentin', 'usage': 'Nerve pain, neuropathy, post-herpetic pain', 'side_effects': 'Drowsiness, dizziness, coordination problems', 'dosage': '300mg-600mg three times daily'},
        {'name': 'Ibuprofen', 'usage': 'Pain, inflammation, fever, arthritis', 'side_effects': 'Stomach upset, heartburn, dizziness', 'dosage': '200mg-400mg every 4-6 hours'},
    ],
}

def get_best_match_drugs(query):
    """Find the best matching drug category for a query"""
    query_lower = query.lower()
    
    # Define keywords for each condition
    keywords = {
        'dengue': ['dengue', 'dengue fever', 'hemor', 'thrombocyt'],
        'asthma': ['asthma', 'asthmatic', 'shortness of breath', 'breathing', 'bronchi', 'copd'],
        'diabetes': ['diabetes', 'diabetic', 'blood sugar', 'glucose', 'insulin'],
        'heart': ['heart', 'cardiac', 'cholesterol', 'hypertension', 'blood pressure', 'bp', 'angina'],
        'allergy': ['allergy', 'allergic', 'hay fever', 'hives', 'rhinitis', 'histamine'],
        'depression': ['depression', 'depressed', 'anxiety', 'anxious', 'panic', 'ocd', 'ptsd', 'mood'],
        'cough': ['cough', 'coughing', 'viral', 'cold', 'expectorant'],
        'infection': ['infection', 'bacterial', 'strep', 'pneumonia', 'uti', 'urinary', 'ear infection'],
        'acid_reflux': ['gerd', 'acid reflux', 'heartburn', 'indigestion', 'reflux', 'ulcer', 'peptic'],
        'pain': ['pain', 'ache', 'sore', 'arthritis', 'rheumatism', 'nerve pain', 'neuropathy'],
    }
    
    # Find matching condition
    best_match = 'default'
    for condition, kw_list in keywords.items():
        for keyword in kw_list:
            if keyword in query_lower:
                best_match = condition
                print(f"  [Match] Query '{query}' matched condition: {condition} (keyword: '{keyword}')")
                return best_match
    
    print(f"  [No Match] Using default drugs")
    return best_match

@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    used_gemini = False
    
    if query:
        print(f"\n{'#'*70}")
        print(f"SEARCH QUERY: '{query}'")
        print(f"{'#'*70}")
        
        # STRATEGY 1: Try Gemini API
        print(f"\n[STEP 1] Calling Gemini API...")
        gemini_results = get_drug_info_from_gemini(query)
        
        has_real_gemini = False
        if gemini_results and len(gemini_results) >= 3:
            first_name = gemini_results[0].get('name', '').lower()
            if first_name and 'treatment options' not in first_name and 'treatment available' not in first_name and 'information' not in first_name:
                has_real_gemini = True
                print(f"✓ Gemini returned {len(gemini_results)} REAL items")
        else:
            print(f"✗ Gemini returned no valid results")
        
        # STRATEGY 2: Try local database
        print(f"\n[STEP 2] Searching local database...")
        db_results = DrugInfo.objects.filter(
            Q(name__icontains=query) | 
            Q(usage__icontains=query)
        ).values('name', 'usage', 'side_effects', 'dosage')
        
        db_list = [dict(r) for r in db_results]
        print(f"✓ Database returned {len(db_list)} items")
        
        # STRATEGY 3: Use intelligent specialized drug matching
        print(f"\n[STEP 3] Matching specialized drug database...")
        matched_condition = get_best_match_drugs(query)
        specialized_drugs = COMMON_DRUGS_DB.get(matched_condition, COMMON_DRUGS_DB['default'])
        print(f"✓ Matched condition: {matched_condition} with {len(specialized_drugs)} drugs")
        
        # DECISION LOGIC
        print(f"\n[DECISION LOGIC]")
        if has_real_gemini and len(gemini_results) >= 3:
            results = gemini_results
            used_gemini = True
            print(f"→ Using Gemini (real results: {len(gemini_results)} items)")
        elif len(db_list) > 0:
            results = db_list
            print(f"→ Using database ({len(db_list)} items)")
        elif len(specialized_drugs) > 0 and matched_condition != 'default':
            results = specialized_drugs
            print(f"→ Using specialized database for '{matched_condition}' ({len(specialized_drugs)} items)")
        elif len(gemini_results) > 0:
            results = gemini_results
            used_gemini = True
            print(f"→ Using Gemini (partial results: {len(gemini_results)} items)")
        else:
            results = COMMON_DRUGS_DB['default']
            print(f"→ Using generic default drugs")
        
        print(f"\n✓✓✓ FINAL RESULT: {len(results)} drugs returned")
        for i, drug in enumerate(results, 1):
            print(f"    {i}. {drug.get('name', 'Unknown')}")
        print(f"{'#'*70}\n")
    
    return render(request, 'drugs/search.html', {
        'results': results,
        'query': query,
        'result_count': len(results),
        'used_gemini': used_gemini
    })
