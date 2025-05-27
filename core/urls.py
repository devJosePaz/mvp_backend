from django.contrib import admin
from django.urls import path, include
from app_login.views import register, home, formulario
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView
from django.views.decorators.http import require_POST

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home page
    path('', home, name='home'),
    # Login/Logout
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', require_POST(LogoutView.as_view()), name='logout'),
    # Cadastro
    path('register/', register, name='register'),
    # Formulario
    path('formulario/', formulario, name='formulario'),
]