from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Environment, Task, Category, Attachment

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

@login_required
def home(request):
    return render(request, 'to_do_list/home/home.html')

@login_required
def environments(request):
    environments = Environment.objects.filter(owner=request.user)
    context = {
        'environments': environments
    }

    return render(request, 'to_do_list/environments/environments.html', context)


@login_required
def create_environment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        owner = request.user

        Environment.objects.create(title=title, description=description, owner=owner)
        return redirect('environments')

    return render(request, 'to_do_list/environments/create_environment.html')


@login_required
def tasks(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()

    if environment:
        tasks = Task.objects.filter(environment=environment)
        context = {
            'environment': environment,
            'tasks': tasks
        }
    else:
        context = {}

    return render(request, 'to_do_list/tasks/tasks.html', context)


@login_required
def create_task(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        Task.objects.create(title=title, description=description, status=status, priority=priority, deadline=deadline, environment=environment)
        return redirect('tasks', environment_id) 

    context = {
        'environment': environment 
    }   

    return render(request, 'to_do_list/tasks/create_task.html', context)


@login_required
def task_detail(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id)

    if task:
        context = {
            'task': task
        }
    else:
        context = {}

    return render(request, 'to_do_list/tasks/task_detail.html', context)


@login_required
def trash(request):
    return HttpResponse('Lixeira')