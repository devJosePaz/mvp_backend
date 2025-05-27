from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import PreferenciasUsuario

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Cria o usuário
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html')



@login_required(login_url='/login/')  # Redundante pois já temos LOGIN_URL, mas é boa prática
def formulario(request):
    if request.method == 'POST':
        PreferenciasUsuario.objects.create(
            usuario=request.user,
            materia=request.POST['materia'],
            nivel=request.POST['nivel'],
            horas_por_semana=request.POST['horas']
        )
        messages.success(request, f"Dados enviados em {timezone.now().strftime('%d/%m/%Y às %H:%M')}")
        return redirect('formulario')
    
    return render(request, 'form.html')