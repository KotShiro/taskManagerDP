from django.db import models
from django.utils import timezone #мы будем получать дату создания todo
from datetime import date
from django.conf import settings 
from accounts.models import User


class Category(models.Model): # Таблица категория которая наследует models.Model
	name = models.CharField(max_length=100) #varchar.Нам потребуется только имя категории
	class Meta:
		verbose_name = ("Category") # человекочитаемое имя объекта
		verbose_name_plural = ("Categories")  #человекочитаемое множественное имя для Категорий
	def __str__(self):
		return self.name  # __str__ применяется для отображения объекта в интерфейсе

class Priority(models.Model): # Таблица категория которая наследует models.Model
	name = models.CharField(max_length=100) #varchar.Нам потребуется только имя категории
	class Meta:
		verbose_name = ("Priority") 
		verbose_name_plural = ("Prioritys") 
	def __str__(self):
		return self.name  # __str__ применяется для отображения объекта в интерфейсе
		
class Task(models.Model):
	title = models.CharField('название задачи', max_length = 200)
	content = models.TextField('текст задачи')
	created = models.DateTimeField('дата создания')
	category = models.ForeignKey(Category, default="general",on_delete=models.PROTECT)# foreignkey с помощью которой мы будем осуществлять связь с таблицей Категорий
	due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) #до какой даты нужно было сделать дело
	priority = models.ForeignKey(Priority, default="general",on_delete=models.PROTECT)
	state = models.BooleanField(default=True)
	director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	executor = models.CharField('Исполнитель', max_length = 200, null=True, blank=True)
	comment = models.TextField('Комментарий к закрытию задачи', null=True, blank=True)
	
	@property
	def is_overdue(self):
		if self.due_date and date.today() > self.due_date:
			return True
		return False
	
	class Meta: #используем вспомогательный класс мета для сортировки наших дел
		ordering = ["-created"] #сортировка дел по времени их создания
	def __str__(self):
		return self.title

	
