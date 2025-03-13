from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date, parse_time
from django.contrib.auth import logout as django_logout, login


from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Task


# Create your views here.
def home(request):
    tasks = Task.objects.all().order_by('-id')

    return render(request, 'index.html', {'tasks': tasks})


def in_work(request):
    work_tasks = Task.objects.filter(work=True)

    return render(request, 'in_work.html', {'tasks': work_tasks}, )


def completed_task(request):
    completed_tasks = Task.objects.filter(completed=True)

    return render(request, 'completed.html', {'tasks': completed_tasks}, )


def remaining(request):
    remaining_tasks = Task.objects.filter(completed=False, work=False)

    return render(request, 'remaining.html', {'tasks': remaining_tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date', '').strip()
        due_time = request.POST.get('due_time', '').strip()

        # Проверяем, что обязательные поля заполнены
        if not title or not due_date or not due_time:
            return render(request, 'add_task.html', {'error': 'Все поля должны быть заполнены'})

        # Парсим дату и время
        due_date_obj = parse_date(due_date)
        due_time_obj = parse_time(due_time)

        if not due_date_obj or not due_time_obj:
            return render(request, 'add_task.html', {'error': 'Неверный формат даты или времени'})

        try:
            task = Task(
                user=request.user, #Привязываем задачу к текущему пользователю
                title=title,
                description=description,
                due_date=due_date_obj,
                due_time=due_time_obj,
                work=False,
                completed=False,
            )
            task.full_clean()  # Запускаем валидацию модели
            task.save()
            return redirect('home')

        except ValidationError as e:
            return render(request, 'add_task.html', {'error': str(e)})
        except IntegrityError:
            return render(request, 'add_task.html', {'error': 'Ошибка базы данных. Попробуйте еще раз.'})

    return render(request, 'add_task.html')


# def add_task(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         due_date = request.POST.get('due_date')
#         due_time = request.POST.get('due_time')
#         work = False
#         completed = False
#
#         if title != '' and due_date != '' and due_time != '':
#             task = Task(
#                 title=title,
#                 description=description,
#                 due_date=due_date,
#                 due_time=due_time,
#                 work=work,
#                 completed=completed,
#             )
#             task.save()
#             return redirect('home')
#     else:
#         return render(request, 'add_task.html')


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'delete.html', {'task': task})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(request, 'task_detail.html', {
        'task': task,
        'owner': task.user  # Передаем владельца задачи в шаблон
    })


@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id,)

    if task:
        task.completed = not task.completed and task.work
        task.work = task.completed or not task.work
        task.save()
        return redirect('home')


@login_required
def remove_task(request, task_id):
    task = get_object_or_404(Task, id=task_id,)
    if task:
        task.delete()
        return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')# Уже авторизован? Перенаправляем.

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    django_logout(request)
    return redirect('home')
