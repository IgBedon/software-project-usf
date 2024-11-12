from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Environment, Task, Category, Attachment


@login_required
def root(request):
    return redirect('login_user')


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
    if request.method == 'POST':
        user = request.user
        User.objects.filter(id=user.id).delete()
        messages.success(request, 'Conta deletada com sucesso!')
        return redirect('account')

    return render(request, 'to_do_list/account/delete_account.html')


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
        return redirect('environments')
    
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
def delete_environment(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':
        environment.delete()
        messages.success(request, 'Ambiente deletado com sucesso!')
        return redirect('environments')
    
    if environment:
        context = {
            'environment': environment,
        }
    else:
        messages.error('Ambiente não encontrado!')
        context={}

    return render(request, 'to_do_list/environments/delete_environment.html', context)


@login_required
def add_collaborator(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':
        collaborator_email = request.POST.get('email')
        user = User.objects.filter(email=collaborator_email).first()

        if user and user != request.user and user not in environment.collaborators.all():
            environment.collaborators.add(user)
            messages.success(request, f'Usuário {user.username} adicionado como colaborador.')
            return redirect('environment', environment_id)
        else:
            messages.warning(request, 'Usuário já é colaborador ou não foi encontrado.')
            return redirect('environment', environment_id)

    context = {
        'environment': environment,
    }
    
    return render(request, 'to_do_list/collaborators/add_collaborator.html', context)


@login_required
def remove_collaborator(request, environment_id):
    environment = Environment.objects.filter(id=environment_id).first()
    collaborators = environment.collaborators.all()

    if request.method == 'POST':
        collaborator_email = request.POST.get('email')
        user = User.objects.get(email=collaborator_email)
        environment.collaborators.remove(user)
        messages.success(request, f'Usuário {user.username} removido dos colaboradores.')
        return redirect('environment', environment_id)

    context = {
        'environment': environment,
        'collaborators': collaborators
    }

    return render(request, 'to_do_list/collaborators/remove_collaborator.html', context)


@login_required
def create_task(request, environment_id):
    environment = get_object_or_404(Environment, id=environment_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')
        attachment = request.FILES.get('attachment')
        
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido.")
            return redirect('create_task', environment_id=environment_id)

        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            deadline=deadline,
            environment=environment
        )

        if attachment:
            Attachment.objects.create(file=attachment, task=task)
        
        messages.success(request, "Tarefa criada com sucesso!")
        return redirect('environment', environment_id=environment_id)

    context = {
        'environment': environment 
    }   

    return render(request, 'to_do_list/tasks/create_task.html', context)


@login_required
def task_detail(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()
    categories = task.categories.all()    
    attachments = task.attachment_set.all()

    if task:
        context = {
            'environment': environment,
            'task': task,
            'categories': categories,
            'attachments': attachments,
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
def add_attachment(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()
    attachments = task.attachment_set.all()

    if request.method == 'POST':
        attachment_file = request.FILES.get('attachment')

        for attachment in attachments:
            if attachment_file.name.split('.')[0] == attachment.title:
                messages.error(request, 'Já existe um arquivo com esse nome!')
                return redirect('task_detail', environment_id, task_id)

        Attachment.objects.create(file=attachment_file, task=task)
        messages.success(request, 'Anexo adicionado com sucesso!')
        return redirect('task_detail', environment_id, task_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/attachment/add_attachment.html', context)


@login_required
def remove_attachment(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()
    attachments = task.attachment_set.all()

    if request.method == 'POST':
        attachment_title = request.POST.get('attachment')
        Attachment.objects.filter(title=attachment_title).delete()
        messages.success(request, 'Anexo removido com sucesso!')
        return redirect('task_detail', environment_id, task_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task,
            'attachments' : attachments
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/attachment/remove_attachment.html', context)


@login_required
def add_category(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()
    categories_environment = environment.category_set.all()
    categories_task = task.categories.all()    
    categories = [category for category in categories_environment if category not in categories_task]

    if request.method == 'POST':
        category_title = request.POST.get('category')
        task.categories.add(Category.objects.get(title=category_title))
        messages.success(request, 'Categoria adicionada com sucesso!')
        return redirect('task_detail', environment_id, task_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task,
            'categories': categories
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/tasks/add_category.html', context)


@login_required
def remove_category(request, environment_id, task_id):
    task = Task.objects.filter(id=task_id).first()
    environment = Environment.objects.filter(id=environment_id).first()
    categories = task.categories.all()

    if request.method == 'POST':
        category_title = request.POST.get('category')
        task.categories.remove(Category.objects.get(title=category_title))
        messages.success(request, 'Categoria removida com sucesso!')
        return redirect('task_detail', environment_id, task_id)
    
    if task:
        context = {
            'environment': environment,
            'task': task,
            'categories': categories
        }
    else:
        messages.error('Tarefa não encontrada!')
        context={}

    return render(request, 'to_do_list/tasks/remove_category.html', context)


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
    category = Category.objects.filter(id=category_id).first()
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
def delete_category(request, environment_id, category_id):
    category = Category.objects.filter(id=category_id).first()
    environment = Environment.objects.filter(id=environment_id).first()

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria deletada com sucesso!')
        return redirect('environment', environment_id)
    
    if category:
        context = {
            'environment': environment,
            'category': category
        }
    else:
        messages.error('Categoria não encontrada!')
        context={}

    return render(request, 'to_do_list/categories/delete_category.html', context)



@login_required
def about_us(request):
    return render(request, 'to_do_list/about_us/about_us.html')