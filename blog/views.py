import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users, Profile
from django.contrib.auth.hashers import make_password
from django.core import serializers
from .models import Blog
from booking.models import Appointment


from datetime import datetime , timedelta
import os.path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



SCOPES = ["https://www.googleapis.com/auth/calendar"]


def home(request):

    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.category == 'patient':
            context = {}
            appointments = Appointment.objects.filter(patient=user).select_related('doctor__profile')
            doctors = Profile.objects.filter(category='doctor')
            context['appointments'] = appointments
            context['profile'] = profile
            context['doctors'] = doctors

            return render(request, 'blog/booking.html', context)

        filter_value = request.GET.get('category')

        if filter_value:

            blogs = Blog.objects.filter(
                drafted=False, category=filter_value).prefetch_related('user')

        else:
            blogs = Blog.objects.filter(drafted=False).prefetch_related('user')

        context = {}
        context['email'] = user.email
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


def blog(request):

    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        user = request.user
        profile = Profile.objects.get(user=user)
        filter_value = request.GET.get('category')

        if filter_value:

            blogs = Blog.objects.filter(
                drafted=False, category=filter_value).prefetch_related('user')

        else:
            blogs = Blog.objects.filter(drafted=False).prefetch_related('user')

        context = {}
        context['email'] = user.email

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

        if filter_value:

            blogs = Blog.objects.filter(
                user=request.user, category=filter_value).prefetch_related('user')

        else:
            blogs = Blog.objects.filter(
                user=request.user).prefetch_related('user')

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
        return render(request, 'blog/create_blog.html', context)
    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def detail_blog(request):

    try:
        if not request.user.is_authenticated:
            return redirect('users.login')
        blog_id = request.GET.get('id')
        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
        blog = Blog.objects.get(id=blog_id)

        context['profile'] = profile
        context['blog'] = blog

        return render(request, 'blog/detail_blog.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def create_appointment(request):
    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        if request.method == 'POST':
            
            date = request.POST.get('date')
            time = request.POST.get('time')
            user = request.user
            doctor_id = request.GET.get('id')
            print(doctor_id, date, time)

            if (doctor_id == '' or date == '' or time == ''):
                messages.error(request, 'Fields cannot be empty')
                print("Fields cannot be empty")
                return redirect('blog.home')
            
            doctor = Profile.objects.get(
                    id=doctor_id)
            
            cred_path = os.path.join(
                os.path.dirname(__file__), "credentials.json")
            creds = None
           
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        cred_path, SCOPES
                    )
            creds = flow.run_local_server(port=0)


            service = build("calendar", "v3", credentials=creds)

            start_datetime = datetime.strptime(date + "T" + time, "%Y-%m-%dT%H:%M")

            end_datetime = start_datetime + timedelta(minutes=45)

           
            end_date = end_datetime.strftime("%Y-%m-%d")
            end_time = end_datetime.strftime("%H:%M")

            event = {
                "summary": "Appointment with " + doctor.firstName + " " + doctor.lastName,
                "location": "Online",
                "description": "Appointment with " + doctor.firstName + " " + doctor.lastName,
                "start": {
                    "dateTime": date + "T" + time + ":00",
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": end_date + "T" + end_time + ":00",
                    "timeZone": "Asia/Kolkata",
                },
                "attendees": [
                    {"email": user.email},
                    {"email": doctor.user.email},
                ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 24 * 60},
                        {"method": "popup", "minutes": 10},
                    ],
                },
            }

            event = service.events().insert(calendarId="primary", body=event).execute()
            print("Event created: %s" % (event.get("htmlLink")))
            messages.success(request, "Appointment Created Successfully")

            appointment = Appointment(doctor=doctor.user, start_date=date, start_time=time, end_time=end_time, patient=user)

            appointment.save()

            

            return redirect('blog.home')


            #Get Request
        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
       
        return render(request, 'blog/create_booking.html', context)
    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")


def my_appointments(request):

    try:
        if not request.user.is_authenticated:
            return redirect('users.login')

        user = request.user
        profile = Profile.objects.get(user=user)

        context = {}
        context['email'] = user.email

        context['profile'] = profile

        if profile.category == 'doctor':
            appointments = Appointment.objects.filter(doctor=user).select_related('doctor__profile').select_related('patient__profile')
        else :
            appointments = Appointment.objects.filter(patient=user).select_related('doctor__profile').select_related('patient__profile')

        context['appointments'] = appointments

        return render(request, 'blog/my_appointments.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")

