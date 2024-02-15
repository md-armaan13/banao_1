from django.urls import path 
from . import views


urlpatterns = [
    path('login/', views.login_users, name='users.login'),
    path('signup/', views.signup_user, name='users.signup'),
    path('logout/', views.logout_users, name='users.logout'),

]
