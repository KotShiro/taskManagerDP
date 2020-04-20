from django.shortcuts import render, redirect #для отображения и редиректа берем необходимые классы
from .models import User
from tasks.models import Task, Category, Priority
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic 
from django.shortcuts import get_object_or_404

from .forms import EditProfileForm

def profile(request, user_id):
	try:
		a = User.objects.get(id = user_id)
	except:
		raise Http404("Пользователь не найдена")
	return render(request, "profile/profile.html", {"user":a})

class LoanedProfileByUser(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view listing books on loan to current user. 
	"""
	model = Task
	template_name ='profile/myProfile.html'
	# queryset = Task.objects.all()
	def get_queryset(self):
		return Task.objects.filter(director=self.request.user).order_by('due_date')

def editProfile(request):
	profile_data = get_object_or_404(User, id=request.user.id)
	edit_form = EditProfileForm(instance=profile_data)
	if request.method == "POST": 
		profile_data.last_name = request.POST["last_name"] 
		profile_data.first_name = request.POST["first_name"] 
		profile_data.fathername = request.POST["fathername"] 
		profile_data.phone = request.POST["phone"] 
		profile_data.email = request.POST["email"] 
		profile_data.save()
		return redirect("/profile")
	return render(request, 'profile/myProfileEdit.html', {'edit_form':edit_form})
	
def allUsersAndAdd(request):
	allUsers = User.objects.all() #запрашиваем все объекты todo через менеджер объектов
	if request.method == "POST": #проверяем то что метод именно POST
		if "Add" in request.POST: #проверяем метод добавления todo
			username = request.POST["username"]
			email = request.POST["email"] 
			password = request.POST["password"] 
			user = User.objects.create_user(username, email, password)
			user.phone = request.POST["phone"] 
			user.last_name = request.POST["last_name"] 
			user.first_name = request.POST["first_name"] 
			user.fathername = request.POST["fathername"] 
			user.save()
			return redirect('accounts:allUsersAndAdd') 
	return render(request, "profile/allProfiles.html", {"allUsers": allUsers})
