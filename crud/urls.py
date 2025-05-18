from django.urls import path
from . import views
from .views import login_view, logout_view, user_list, gender_list

urlpatterns = [
    path('gender/list', views.gender_list, name='gender_list'), # protected
    path('gender/add', views.add_gender, name='add_gender'), # protected
    path('gender/edit/<int:genderId>', views.edit_gender, name='edit_gender'), # protected
    path('gender/delete/<int:genderId>', views.delete_gender), # protected
    path('user/list', views.user_list), # protected
    path('user/add', views.add_user), # protected
    path('user/edit/<int:userId>', views.user_edit), # protected
    path('user/delete/<int:userId>', views.user_delete), # protected
    path('', login_view, name='home'), # public
    path('login/', login_view, name='login'), # public
    path('logout/', logout_view, name='logout') # protected
]