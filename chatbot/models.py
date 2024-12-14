from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    SESSION_CHOICES = [
        ('default', 'Default Session'),
        ('important', 'Important Session'),
        ('archived', 'Archived Session'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=255, choices=SESSION_CHOICES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Indicates active sessions
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session for {self.user.username} - {self.session_name}"

    def get_latest_chat(self):
        return self.chat_set.latest('created_at')

    class Meta:
        ordering = ['-created_at']

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processed', 'Processed')], default='pending')

    def __str__(self):
        return f"Chat {self.id} - {self.user.username}: {self.message[:50]}..."

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['created_at']

class UserHistory(models.Model):
    ACTION_CHOICES = [
        ('sent_message', 'Sent Message'),
        ('viewed_history', 'Viewed History'),
        ('logged_in', 'Logged In'),
        ('logged_out', 'Logged Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

