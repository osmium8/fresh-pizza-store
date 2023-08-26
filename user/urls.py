from django.urls import path
from user.views import LogoutAPIView, RegisterView, IsAuthenticatedAPIView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('isauthenticated/', IsAuthenticatedAPIView.as_view())
]