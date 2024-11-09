from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Environment, Task, Category, Attachment


@login_required
def root(request):
    return HttpResponse("Welcome to Easy Task")


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
        return redirect('environments')

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
                    return redirect('environments') 
        except:
            pass
    
        messages.error(request, 'Credenciais inválidas. Tente novamente.')
        return redirect('login_user')
    
    return render(request, 'to_do_list/signin_login/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required
def account(request):
    user = request.user
    context = {
        'user': user
    }

    return render(request, "to_do_list/account/account.html", context)


@login_required
def update_account(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        User.objects.filter(id=user.id).update(username=username, email=email)
        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('account')
        

    context = {
        'username' : user.username,
        'email': user.email,
        'password': user.password
    }

    return render(request, 'to_do_list/account/update_account.html', context)


@login_required
def delete_account(request):
    pass


@login_required
def update_account_password(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        password = request.POST.get('password')
        user_password = authenticate(username=user.username, password=password)

        if user_password is not None:
            new_password = request.POST.get('new_password')
            new_password_check = request.POST.get('new_password_check')

            if new_password == new_password_check:
                user.set_password(new_password)
                user.save()
                login(request, user)

                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('account')
            
            messages.error(request, 'As senhas a serem inseridas não coincidem. Tente novamente.')
            return redirect('update_account_password')
        
        messages.error(request, 'A senha atual está incorreta. Tente novamente.')
        return redirect('update_account_password')

    return render(request, 'to_do_list/account/update_account_password.html')


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
def environment_selected(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()

    if environment:
        tasks = Task.objects.filter(environment=environment)
        categories = Category.objects.filter(environment=environment)
        context = {
            'environment': environment,
            'tasks': tasks,
            'categories': categories
        }
    else:
        messages.error('Ambiente não encontrado!')
        context = {}

    return render(request, 'to_do_list/environments/environment.html', context)


@login_required
def update_environment(request, environment_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Environment.objects.filter(id=environment_id).update(title=title, description=description)
        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('environment', environment_id)
    
    environment = Environment.objects.filter(id=environment_id).first()
    if environment:
        context = {
            'environment': environment
        }
    else:
        messages.error('Ambiente não encontrado!')
        context={}

    return render(request, 'to_do_list/environments/update_environment.html', context)


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
        return redirect('environment', environment_id) 

    context = {
        'environment': environment 
    }   

    return render(request, 'to_do_list/tasks/create_task.html', context)


@login_required
def task_detail(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()

    if task:
        context = {
            'environment': environment,
            'task': task
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/tasks/task_detail.html', context)


@login_required
def update_task(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        Task.objects.filter(id=task_id).update(title=title, description=description, status=status, priority=priority, deadline=deadline)
        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('environment', environment_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}


    return render(request, 'to_do_list/tasks/update_task.html', context)


@login_required
def delete_task(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':

        task.delete()
        messages.success(request, 'Tarefa deletada com sucesso!')
        return redirect('environment', environment_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/tasks/delete_task.html', context)

@login_required
def create_category(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        color = request.POST.get('color')

        Category.objects.create(title=title, description=description, color=color, environment=environment)
        return redirect('environment', environment_id) 

    context = {
        'environment': environment 
    }   

    return render(request, 'to_do_list/categories/create_category.html', context)


@login_required
def category_detail(request, environment_id, category_id):
    category = Category.objects.filter(id=category_id)
    environment = Environment.objects.filter(id=environment_id).first()

    if category:
        context = {
            'environment': environment,
            'category': category
        }
    else:
        messages.error('Categoria não encontrada!')
        context = {}

    return render(request, 'to_do_list/categories/category_detail.html', context)


@login_required
def update_category(request, environment_id, category_id):
    category = Category.objects.filter(id=category_id).first()
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        color = request.POST.get('color')

        Category.objects.filter(id=category_id).update(title=title, description=description, color=color)
        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('environment', environment_id) 

    if category:
        context = {
            'environment': environment,
            'category': category
        }
    else:
        messages.error('Categoria não encontrada!')
        context = {}

    return render(request, 'to_do_list/categories/update_category.html', context)


@login_required
def about_us(request):
    return HttpResponse('Sobre nós')