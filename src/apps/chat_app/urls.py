from django.urls import path
from apps.chat_app.views import index

urlpatterns = [
    path('', index)
]