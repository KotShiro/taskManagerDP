from django.urls import path
from django.conf.urls import url

from . import views
from .views import LoanedTasksByUserListView, newTask
 
app_name = 'tasks'
urlpatterns = [
	path('', views.tasksPage, name='tasksPage'),
	path('<int:task_id>/',views.detail, name = 'detail'),
	path('new', newTask, name='newTask'),
]

urlpatterns += [   
    url(r'^my/$', views.LoanedTasksByUserListView.as_view(), name='my-borrowed'),
]