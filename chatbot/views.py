from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .models import Chat, Session, UserHistory
import requests
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)
# chatbot/views.py
from django.http import JsonResponse
from .utils import generate_text_with_gemini  # Assuming you have the generate_text_with_gemini function in utils.py

def generate_gemini_response(request):
    if request.method == 'POST':
        try:
            # Get the message from the frontend
            data = json.loads(request.body)
            message = data.get('message')

            # Get the response from Gemini API
            response = generate_text_with_gemini(message)

            # Return the response back to the frontend as JSON
            return JsonResponse({'response': response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Home view
def home(request):
    return render(request, 'home.html')

# Chatbot view to handle chat sessions
@login_required
def chatbot(request, session_id=None):
    """
    Handle chat interactions and manage sessions for logged-in users.
    """
    try:
        # Retrieve or create a session
        if session_id:
            active_session = Session.objects.get(id=session_id, user=request.user)
        else:
            active_session, _ = Session.objects.get_or_create(user=request.user)

        # Retrieve existing chat history for the session
        chats = Chat.objects.filter(session=active_session).order_by('created_at')

        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')

            if not message:
                return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

            # Generate response using Google Gemini
            response = generate_text_with_gemini(message)

            # Save chat to the database
            chat = Chat.objects.create(
                session=active_session,
                user=request.user,
                message=message,
                response=response,
                created_at=timezone.now(),
            )

            # Log user history
            UserHistory.objects.create(
                user=request.user,
                action=f"Sent message: {message}",
                timestamp=timezone.now(),
            )

            return JsonResponse({'message': message, 'response': response})

        # Render chatbot interface
        sessions = Session.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'chatbot.html', {'chats': chats, 'session': active_session, 'sessions': sessions})

    except Exception as e:
        logger.error(f"Chatbot view error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

# Create a new chat session
@login_required
def new_chat(request):
    """
    Start a new chat session for the logged-in user.
    """
    new_session = Session.objects.create(user=request.user)
    return redirect(reverse('chatbot', kwargs={'session_id': new_session.id}))

# User login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect to active session or create a new one
            active_session = Session.objects.filter(user=user).first()
            if not active_session:
                active_session = Session.objects.create(user=user)
            return redirect('chatbot', session_id=active_session.id)

        messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('chatbot')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User logout
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# Load session history
@login_required
def load_session_history(request, session_id):
    try:
        session = Session.objects.get(id=session_id, user=request.user)
        chats = Chat.objects.filter(session=session).order_by('created_at')

        chat_data = [
            {
                'user': 'You' if chat.user == request.user else chat.user.username,
                'message': chat.message,
                'response': chat.response,
            }
            for chat in chats
        ]
        return JsonResponse({'chats': chat_data})
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found.'}, status=404)
    except Exception as e:
        logger.error(f"Error loading session history: {str(e)}")
        return JsonResponse({'error': 'Failed to load session history.'}, status=500)
@login_required
def history_view(request):
    """
    Display all chat sessions for the logged-in user with basic session details.
    """
    try:
        # Fetch the chat sessions for the logged-in user
        user_sessions = Session.objects.filter(user=request.user).order_by('-created_at')

        # Include session details such as total chats
        sessions = [
            {
                'id': session.id,
                'created_at': session.created_at,
                'chat_count': Chat.objects.filter(session=session).count(),
            }
            for session in user_sessions
        ]

        return render(request, 'history.html', {'sessions': sessions})

    except Exception as e:
        logger.error(f"Error in history_view: {str(e)}")
        messages.error(request, "Failed to load chat history.")
        return render(request, 'history.html', {'sessions': []})