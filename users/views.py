from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .models import Users , Profile
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def home(request):

    try :
        if  not request.user.is_authenticated:
            return redirect('users.login')  
      
        context = {}
        user = request.user
        context['email'] = user.email
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        print(context)
        return render(request,'users/index.html',context)
      
    except  Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")
    
def login_users(request):

    if request.user.is_authenticated:
        return redirect('users.home')
    try : 
        if request.method == 'POST':
            
            email = request.POST.get('email')
            password = request.POST.get('password')

            if(email == '' or password == ''):
                messages.error(request, 'Fields cannot be empty')
                return redirect('users.login')
            
            user = authenticate(request , username=email , password=password)
            if user is not None:
                login(request , user)
                return redirect('users.home')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('users.login')
        
        else :
            return render(request,'registration/login.html')
    except  Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")

def signup_user(request):
    try:
        if request.user.is_authenticated:
            return redirect('users.home')
        
        if request.method == 'POST':
           
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password= request.POST.get('confirm_password')
            category = request.POST.get('category')
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            username = request.POST.get('username')
            image = request.FILES.get('image')
    
            if 'image' in request.FILES:
                image = request.FILES['image']
            else:
                image = None 

        
            if(email == '' or password == '' or confirm_password == '' or firstName == '' or lastName == '' or address == '' or city == '' or state == '' or pincode == '' or category == '' or username == '' or image == None):
                messages.error(request, 'Fields cannot be empty')
                print("Fields cannot be empty")
                return redirect('users.signup')
            # Validate email
            try:
                validate_email(email)
            except ValidationError:
                print("Invalid email")
                messages.error(request, 'Invalid email')
                return render(request, 'registration/signup.html')
            if(password != confirm_password):
                print("Passwords do not match")
                messages.error(request, 'Passwords do not match')
                return redirect('users.signup')
            
            if(Users.objects.filter(email=email).exists()):
                messages.error(request, 'Email already exists')
                print("Email already exists")
                return redirect('users.signup')
            
            hashed_password = make_password(password)  # Hash the password
            tempUser = Users(email=email, password=hashed_password)
            tempUser.save()

            print(tempUser.id)

            profile = Profile(username=username, firstName=firstName, lastName=lastName, image=image, category=category, user=tempUser, address=address, city=city, state=state, pincode=pincode)
            
            profile.save()

            
            messages.success(request, 'Account created successfully')
            return redirect('users.login')
        
        return render(request,'registration/registration.html')
    except  Exception as e:
        print(e)
        return HttpResponse("ERROR 404 NOT FOUND")

def logout_users(request):
    if request.user.is_authenticated:

        logout(request)
        return redirect('users.login')
    else:
        return redirect('users.login')