from django.urls import path
from django.conf.urls import url

from .views import profile, LoanedProfileByUser, editProfile, allUsersAndAdd
from . import views
 
app_name = 'accounts'
urlpatterns = [
	path('', LoanedProfileByUser.as_view(), name='my-profile'),
	path('edit', editProfile, name='editProfile'),
	path('<int:user_id>/', profile , name = 'profile'),
	path('all', allUsersAndAdd , name = 'allUsersAndAdd'),
]

# urlpatterns += [   
	# url(r'^myProfile/$', LoanedProfileByUser.as_view(), name='my-profile'),
# ]