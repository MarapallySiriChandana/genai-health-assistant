from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
from django.conf import settings
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

@login_required
def chat_view(request):
    if request.method == 'POST':
        user_query = request.POST.get('query')
        if user_query:
            # Initialize model
            try:
                model = genai.GenerativeModel('gemini-flash-latest', 
                    system_instruction="You are a healthcare assistant. Provide safe, general medical advice. Do NOT give final diagnosis. Always suggest consulting a professional doctor for serious concerns. Keep responses concise and helpful.")
                
                # Build history for context (Session memory)
                # Retrieve LAST 10 messages from DB for this user, then reverse to chronological
                past_messages = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
                history = []
                # reverse the queryset objects list
                for chat in reversed(list(past_messages)):
                    history.append({"role": "user", "parts": [chat.query]})
                    history.append({"role": "model", "parts": [chat.response]})
                
                # Start chat with history
                chat_session = model.start_chat(history=history)
                
                response = chat_session.send_message(user_query)
                ai_response = response.text
                
            except Exception as e:
                ai_response = f"Communication Error: {str(e)}"
            
            # Save to DB (Always save so history shows the error if it occurred)
            ChatHistory.objects.create(
                user=request.user,
                query=user_query,
                response=ai_response
            )
        
    # Get chat history to display in UI (Newest first is fine for flex-direction: column-reverse)
    chats = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chatbot/chat.html', {'chats': chats})
