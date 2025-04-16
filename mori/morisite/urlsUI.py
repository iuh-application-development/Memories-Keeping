from django.urls import path
from .templateUI import *

urlpatterns = [    
    # landing
    path("landing", landing),
    
    # auth
    path("login", loginUI),
    path("register", register),
    path("forgot-password", forgot_password),
    
    # dashboard
    path("admin", adminUI),
    
    path("home", home),
    
    path("manage-imgs", manage_imgs),
    
    path("history-imgs", history_imgs),
    
    path("social", social),
    
    path("history-imgs", history_imgs),
    
    path("imgs", imgs),
    
    path("profile", profile),
    
    path("trash", trash),
    
    
    # API UI
    path('api/objects/', Objects.as_view(), name='objects'),
    path('api/colors/', Colors.as_view(), name='colors'),
]
