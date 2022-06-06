from django import views
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('v1/projects/', views.getProjects),
    path('v1/projects/<str:pk>/', views.getSingleProject),
]