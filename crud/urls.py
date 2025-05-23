from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_view, name='login'), # public
    path('logout/', views.logout_view, name='logout'),
    path('gender/list/', views.gender_list, name='gender_list'), # protected
    path('gender/add/', views.add_gender, name='add_gender'), # protected
    path('gender/edit/<int:genderId>/', views.edit_gender, name='edit_gender'), # protected
    path('gender/delete/<int:genderId>/', views.delete_gender), # protected
    path('user/list/', views.user_list), # protected
    path('user/add/', views.add_user), # protected
    path('user/edit/<int:userId>/', views.user_edit), # protected
    path('user/delete/<int:userId>/', views.user_delete), # protected
    path('', views.home),
    path('user/change_password/<int:user_id>/', views.change_password, name='change_password')
]