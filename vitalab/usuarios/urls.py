from django.urls import path
from . import views

app_name = "usuarios"
urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.user_login, name='login'),
]
