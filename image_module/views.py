from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ImageAnalysis
from django.conf import settings
import google.generativeai as genai
from PIL import Image
import os

genai.configure(api_key=settings.GEMINI_API_KEY)

@login_required
def upload_view(request):
    analysis_result = None
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Save analysis object with image
        analysis = ImageAnalysis.objects.create(
            user=request.user,
            image=image_file
        )
        
        # Process with Gemini Vision
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            img = Image.open(analysis.image.path)
            
            prompt = "Analyze this medical image and provide general insights. Mention possible observations but do not give a final diagnosis. Advise the user to see a doctor."
            
            response = model.generate_content([prompt, img])
            analysis.analysis_result = response.text
            analysis.save()
            analysis_result = response.text
        except Exception as e:
            analysis_result = f"Error analyzing image: {str(e)}"
            analysis.analysis_result = analysis_result
            analysis.save()

    # Get user's recent analyses
    history = ImageAnalysis.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'image_module/upload.html', {'history': history, 'result': analysis_result})
