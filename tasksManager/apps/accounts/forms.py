from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import User

class EditProfileForm(forms.ModelForm):
    '''Форма задачи к статьям'''
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'fathername',  'phone', 'email',)


