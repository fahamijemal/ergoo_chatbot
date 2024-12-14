from django.urls import include, path
from . import views
from django.contrib import admin 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('chatbot/<int:session_id>/', views.chatbot, name='chatbot'),  # Update here to accept session_id
    path('chatbot/new/', views.new_chat, name='new_chat'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='history'),
    path('chatbot/history/<int:session_id>/', views.load_session_history, name='load_session_history'),
    path('generate-gemini-response/', views.generate_gemini_response, name='generate_gemini_response'),
]
