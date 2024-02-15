from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Users, Profile
from django.contrib.auth.hashers import make_password
from django.core import serializers
from .models import Blog


def home(request):

    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        filter_value = request.GET.get('category')
        print(filter_value)

        if filter_value:
            
            blogs = Blog.objects.filter(
                drafted=False, category=filter_value).prefetch_related('user')

        else:
            blogs = Blog.objects.filter(drafted=False).prefetch_related('user')

        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)

        context['profile'] = profile
        for blog in blogs:
            blog.created_at = blog.created_at.strftime("%b %d %Y")
            words = blog.summary.split()

            if (len(words) > 15):
                words = words[:15]
                blog.summary = ' '.join(words) + '...'

        context['blogs'] = blogs
        return render(request, 'blog/index.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def my_blog(request):
    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        filter_value = request.GET.get('category')
        print(filter_value)

        if filter_value:
            
            blogs = Blog.objects.filter(user=request.user, category=filter_value).prefetch_related('user')

        else:
            blogs = Blog.objects.filter(user=request.user).prefetch_related('user')

        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
       
        context['profile'] = profile


        for blog in blogs:

            blog.created_at = blog.created_at.strftime("%b %d %Y")
            words = blog.summary.split()

            if (len(words) > 15):
                words = words[:15]
                blog.summary = ' '.join(words) + '...'

        context['blogs'] = blogs
        return render(request, 'blog/my_blog.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def profile(request):
    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
       
        context['profile'] = profile
        print(context)
        return render(request, 'blog/profile.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def create_blog(request):
    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        if request.method == 'POST':
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            category = request.POST.get('category')
            image = request.FILES.get('image')
            drafted = request.POST.get('drafted')
            user = request.user
            print(title, summary, content, category, image, drafted, user)

            if drafted == 'on':
                drafted = True
            else:
                drafted = False

            if 'image' in request.FILES:
                image = request.FILES['image']
            else:
                image = None
            if (title == '' or summary == '' or content == '' or category == '' or image == None or drafted == None or drafted == ''):
                messages.error(request, 'Fields cannot be empty')
                print("Fields cannot be empty")
                return redirect('blog.create-blog')

            blog = Blog(title=title, summary=summary, content=content,
                        category=category, image=image, drafted=drafted, user=user)
           
            blog.save()
            return redirect('blog.home')
        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        print(context)
        return render(request, 'blog/create_blog.html',context)
    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def detail_blog(request):
   
    try :
        if  not request.user.is_authenticated:
            return redirect('users.login')
        blog_id = request.GET.get('id')
        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
        blog = Blog.objects.get(id=blog_id)
       
        context['profile'] = profile
        context['blog'] = blog
        
        return render(request,'blog/detail_blog.html',context)

    except  Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")
