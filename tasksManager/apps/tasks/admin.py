from django.contrib import admin
from .models import Task, Category, Priority
#textEditor
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Task, PostAdmin)
admin.site.register(Category)
admin.site.register(Priority)



