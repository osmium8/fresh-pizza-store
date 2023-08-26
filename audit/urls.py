from django.urls import path
from audit.views import OrderStatusView

urlpatterns = [
    path('track/<int:pk>/', OrderStatusView.as_view(), name='track placed order'),
]