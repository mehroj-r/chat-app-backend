from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("users/", include("apps.account.api.urls", namespace="users")),
    path("chats/", include("apps.chat.api.urls", namespace="dashboard")),
    path("auth/",
         include(
            [
                path('login/', TokenObtainPairView.as_view(), name='login'),
                path('refresh/', TokenRefreshView.as_view(), name='refresh'),
                path('verify/', TokenVerifyView.as_view(), name='verify'),
            ],
    )),
]