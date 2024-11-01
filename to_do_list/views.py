from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

def health_check(request):
    return HttpResponse('Web Server is online!')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verifica se as senhas coincidem
        if password1 != password2:
            messages.error(request, "As senhas não coincidem")
            return redirect('register_user')

        # Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso")
            return redirect('register_user')

        # Verifica se o e-mail já está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "E-mail já está em uso")
            return redirect('register_user')

        # Cria o novo usuário
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Realiza login automático
        login(request, user)
        messages.success(request, f"Cadastro realizado com sucesso! Bem-vindo, {user.username}.")
        return redirect('home')

    return render(request, 'to_do_list/signin_login/register.html')

    
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            existing_user = User.objects.get(email=email)
            if existing_user:
                user = authenticate(request, username=existing_user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home') 
        except:
            pass
    
        messages.error(request, 'Credenciais inválidas. Tente novamente.')
        return redirect('login_user')
    
    return render(request, 'to_do_list/signin_login/login.html')


def home(request):
    return render(request, 'to_do_list/home/home.html')


def environments(request):
    return render(request, 'to_do_list/environments/environments.html')


def create_environment(request):
    if request.method == 'POST':
        pass

    return render(request, 'to_do_list/environments/create_environment.html')


def trash(request):
    return HttpResponse('Lixeira')