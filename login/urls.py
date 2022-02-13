from django.urls import path
from .views import Login, LogoutView as Logout, RegisterView, edit
from django.contrib.auth import views as auth_view

app_name = 'login'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', edit, name='edit'),
]