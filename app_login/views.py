from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import PreferenciasUsuario
from app_ia.algoritmo_ia.services import IARecommendationService

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



@login_required
def formulario(request):
    ia_service = IARecommendationService()
    
    if request.method == 'POST':
        # Cria e salva as preferências
        preferencia = PreferenciasUsuario(
            usuario=request.user,
            materia=request.POST['materia'],
            nivel=request.POST['nivel'],
            horas=float(request.POST['horas'])
        )
        
        # Gera as recomendações
        recomendacoes = ia_service.gerar_recomendacoes({
            "materia": preferencia.materia,
            "nivel": preferencia.nivel,
            "horas": preferencia.horas
        })
        
        if recomendacoes:
            preferencia.recomendacoes = recomendacoes
            preferencia.save()
            messages.success(request, "Plano de estudo gerado com sucesso!")
        else:
            messages.error(request, "Erro ao gerar recomendações")
        
        return redirect('formulario')
    
    # Busca a última recomendação do usuário
    ultima_recomendacao = PreferenciasUsuario.objects.filter(
        usuario=request.user
    ).exclude(recomendacoes__isnull=True).order_by('-criado_em').first()
    
    return render(request, 'form.html', {
        'recomendacao': ultima_recomendacao.recomendacoes if ultima_recomendacao else None
    })