from django import forms
from .models import Task, List

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1,'placeholder': 'Enter list title...','class': 'form-control', }),           
            'description': forms.Textarea(attrs={'rows': 1,'placeholder': 'Enter list description...','class': 'form-control',
            })}

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['list', 'title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),

        }
