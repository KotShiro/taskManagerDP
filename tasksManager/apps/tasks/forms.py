from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Task, Category, Priority #не забываем наши модели
from accounts.models import User
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Task, Category, Priority #не забываем наши модели

class TaskForm(forms.ModelForm):
    '''Форма задачи к статьям'''
    class Meta:
        model = Task
        fields = ['content']
        widgets = {
            'content': SummernoteWidget(),
}   

class CommentForm(forms.ModelForm):
    '''Форма комментария к задаче'''
    class Meta:
        model = Task
        fields = ['comment']
        widgets = {
            'comment': SummernoteWidget(),
}