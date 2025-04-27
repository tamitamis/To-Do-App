from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, List
from .forms import TaskForm, ListForm

def list_list(request):
    lists = List.objects.all()
    return render(request, 'tasks/list_list.html', {'lists': lists})

def list_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_list')
    else:
        form = ListForm()
    return render(request, 'tasks/list_form.html', {'form': form})

def list_delete(request, pk):
    list_obj = get_object_or_404(List, pk=pk)
    if request.method == 'POST':
        list_obj.delete()
        return redirect('list_list')
    return render(request, 'tasks/list_confirm_delete.html', {'list': list_obj})

import datetime
from django.utils import timezone

from django.contrib import messages

def task_list(request, list_pk):
    list_obj = get_object_or_404(List, pk=list_pk)
    tasks = list_obj.tasks.all().order_by('due_date')
    if request.method == "POST":
        title_str = request.POST.get('title')
        if title_str:
            titles = title_str.split(',')
            description = request.POST.get('description', '')
            due_date = request.POST.get('due_date')
            for title in titles:
                Task.objects.create(list=list_obj, title=title.strip(), description=description, due_date=due_date)
            return redirect('task_list', list_pk=list_pk)
        else:
            # Handle the case where title is missing or empty
            messages.error(request, "Task title is required.")
            return redirect('task_list', list_pk=list_pk)
    form = TaskForm(initial={'list': list_obj})

    # Calculate tomorrow's date
    tomorrow = timezone.now().date() + datetime.timedelta(days=1)
    due_tomorrow_tasks = tasks.filter(due_date=tomorrow, done=False)

    if due_tomorrow_tasks.exists():
        messages.info(request, f"You have {due_tomorrow_tasks.count()} task(s) due tomorrow.")

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'form': form,
        'list': list_obj,
    })

def toggle_task(request, list_pk, pk):
    task = get_object_or_404(Task, pk=pk, list_id=list_pk)
    task.done = not task.done
    task.save()
    return redirect('task_list', list_pk=list_pk)

def delete_task(request, list_pk, pk):
    task = get_object_or_404(Task, pk=pk, list_id=list_pk)
    task.delete()
    return redirect('task_list', list_pk=list_pk)
