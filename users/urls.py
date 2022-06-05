from django.urls import path
from . import views

urlpatterns=[
    path("", views.profiles, name="profiles"),

    path("profile/<str:pk>", views.userProfile, name="user-profile"),
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    
    path("register/", views.register_auth, name="register"),
    path("login/", views.login_auth, name="login"),
    path("logout/", views.logout_auth, name="logout"),
]