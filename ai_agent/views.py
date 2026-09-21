from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import run_study_mate_agent

@login_required
def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
            
        try:
            bot_response = run_study_mate_agent(request.user, user_message)
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'response': f"حدث خطأ أثناء معالجة الطلب: {str(e)}"}, status=500)
            
    return JsonResponse({'error': 'Invalid method'}, status=405)

