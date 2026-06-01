from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from chatbot.models import ChatHistory
from ml_module.models import SymptomPrediction
from image_module.models import ImageAnalysis

@staff_member_required
def dashboard(request):
    stats = {
        'total_users': User.objects.count(),
        'total_chats': ChatHistory.objects.count(),
        'total_predictions': SymptomPrediction.objects.count(),
        'total_images': ImageAnalysis.objects.count(),
    }
    recent_chats = ChatHistory.objects.all()[:5]
    recent_predictions = SymptomPrediction.objects.all()[:5]
    
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_chats': recent_chats,
        'recent_predictions': recent_predictions,
    })

@staff_member_required
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})

@staff_member_required
def chat_logs(request):
    chats = ChatHistory.objects.all().select_related('user')
    return render(request, 'admin_panel/chats.html', {'chats': chats})

@staff_member_required
def predictions(request):
    preds = SymptomPrediction.objects.all().select_related('user')
    return render(request, 'admin_panel/predictions.html', {'predictions': preds})

@staff_member_required
def image_analyses(request):
    analyses = ImageAnalysis.objects.all().select_related('user')
    return render(request, 'admin_panel/images.html', {'analyses': analyses})

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "Cannot delete a superuser.")
    else:
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")
    return redirect('admin_panel:manage_users')
