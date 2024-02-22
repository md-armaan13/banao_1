from django.urls import path 
from . import views


urlpatterns = [
    path('',views.home , name= "blog.home"),
    path('blog/',views.blog , name= "blog.blog"),
    path('my-blog/',views.my_blog , name= "blog.my-blog"),
    path('profile/',views.profile , name= "blog.profile"),
    path('create-blog/',views.create_blog , name= "blog.create-blog"),
    path('detail-blog/',views.detail_blog , name= "blog.detail-blog"),
    path('create-appointment/',views.create_appointment , name= "blog.create-appointment"),
    path('appointment/',views.my_appointments , name= "blog.appointment"),
    
]
