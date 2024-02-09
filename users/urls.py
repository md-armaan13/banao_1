from django.urls import path 
from . import views


urlpatterns = [
    path('',views.home , name= "users.home"),
    path('auth/login/', views.login_users, name='users.login'),
    path('auth/signup/', views.signup_user, name='users.signup'),
    path('auth/logout/', views.logout_users, name='users.logout'),

]
