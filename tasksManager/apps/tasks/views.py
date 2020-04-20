# необходимые HTTP и прочее проекта
from django.shortcuts import render, redirect #для отображения и редиректа берем необходимые классы
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings 
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone 
from datetime import date
##############################################
#подключение моделей
from .models import Task, Category, Priority
from accounts.models import User
##############################################
#Формы
from .forms import TaskForm, CommentForm
##############################################
#подключения для пользователей
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group
##############################################

# глаынй редирект
def redirect_view(request):
	return redirect("/tasks") # редирект с главной на категории

def tasksPage(request):
	todos = Task.objects.all() #запрашиваем все объекты todo через менеджер объектов
	categories = Category.objects.all() #так же получаем все Категории	
	prioritys = Priority.objects.all() #так же получаем все Категории

	return render(request, "tasks/allTasks.html", {"todos": todos, "categories": categories, "prioritys": prioritys})

def newTask(request):
	todos = Task.objects.all() #запрашиваем все объекты todo через менеджер объектов
	categories = Category.objects.all() #так же получаем все Категории	
	prioritys = Priority.objects.all() #так же получаем все Категории
	form = TaskForm()
	if request.method == "POST": #проверяем то что метод именно POST
		if "Add" in request.POST: #проверяем метод добавления todo
			title = request.POST["description"] #сам текст
			date = str(request.POST["date"]) #дата, до которой должно быть закончено дело
			category = request.POST["category_select"] #категория, которой может выбрать или создать пользователь.
			created = timezone.now()
			content = request.POST["content"] 
			priority = request.POST["priority_select"]
			directorName = str(request.POST["directorName"])
			Todo = Task(title=title, content=content, due_date=date, created = created, priority=Priority.objects.get(name=priority),
			category=Category.objects.get(name=category), director = User.objects.get(username__exact=directorName), state = True)
			Todo.save() # сохранение нашего дела
			return redirect("/todo") # перегрузка страницы (ну вот так у нас будет устроено очищение формы)
		if "Delete" in request.POST: #если пользователь собирается удалить одно дело
			checkedlist = request.POST.getlist('checkedbox') # берем список выделенные дел, которые мы собираемся удалить
			for i in range(len(checkedlist)): #мне почему-то не нравится эта конструкция
				todo = Task.objects.filter(id=int(checkedlist[i]))
				todo.delete() #удаление дела
	return render(request, "tasks/newTask.html", {"todos": todos, "categories": categories, "prioritys": prioritys, "form": form})
	


def category(request):
	categories = Category.objects.all()  #запрашиваем все объекты Категорий
	prioritys = Priority.objects.all()  #запрашиваем все объекты Приоритета
	if request.method == "POST": #проверяем что это метод POST
		if "Add" in request.POST: #если собираемся добавить
			name = request.POST["name"] #имя нашей категории
			category = Category(name=name) #у нашей категории есть только имя
			category.save() # сохранение нашей категории
			return redirect("/category")
		if "Delete" in request.POST: # проверяем есть ли удаление
			check = request.POST.getlist('check') #немного изменил название массива в отличии от todo, что бы было меньше путаницы в коде
			for i in range(len(check)):
				try:
					сateg = Category.objects.filter(id=int(check[i]))
					сateg.delete()   #удаление категории
				except BaseException: # вне сомнения тут нужно нормально переписать обработку ошибок, но на первое время хватит и этого
					return HttpResponse('<h1>Сначала удалите карточки с этими категориями)</h1>')
	return render(request, "tasks/category.html", {"categories": categories, "prioritys": prioritys})	
	
def detail(request, task_id):
	formComment = CommentForm()
	
	try:
		a = Task.objects.get(id = task_id)
	except:
		raise Http404("Задача не найдена")
	if request.method == "POST": #проверяем то что метод именно POST
		if "Completed" in request.POST:
			comment = request.POST["comment"] 
			IdExecutor = request.POST["IdExecutor"]
			executor = User.objects.get(id=IdExecutor)
			full_name = executor.first_name + ' ' + executor.last_name 
			a.comment = comment
			a.executor = str(full_name)
			a.state = False
		a.save()
	return render(request, "tasks/detail.html", {"task":a, "formComment": formComment})
	
class LoanedTasksByUserListView(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view listing books on loan to current user. 
	"""
	model = Task
	template_name ='tasks/myTasks.html'
	paginate_by = 10

	def get_queryset(self):
		return Task.objects.filter(director=self.request.user).order_by('due_date')
	
