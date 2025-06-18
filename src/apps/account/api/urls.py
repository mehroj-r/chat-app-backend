from django.urls import path

from .views import UserRegistrationView, CurrentUserView, UserSearchView, UpdateProfileView

app_name = "account"
urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('update-profile/', UpdateProfileView.as_view()),
]