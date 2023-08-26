from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Internal Applications
    path('api/pizzeria/', include("pizzeria.urls")),
    path('api/auth/', include("user.urls")),
    path('api/audit/', include("audit.urls")),
    # External Packages
    path('api/auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]