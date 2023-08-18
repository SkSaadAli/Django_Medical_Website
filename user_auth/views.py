from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserSignupForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from user_auth.decorators import patient_required, doctor_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# utility functions
def check_confirm_password(form):
    if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
        return True
    return False

def redirect_to_dashboard(user):
    if user.profile_type == 'Patient' or user.profile_type == 'patient':
        return 'patient_dashboard'  # Replace with your patient dashboard URL name
    elif user.profile_type == 'Doctor' or user.profile_type == 'doctor':
        return 'doctor_dashboard'  # Replace with your doctor dashboard URL name

# all the urls

def home(request):
    return render(request, 'base.html')

def signup(request):
   
    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)   
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(commit=False)

            if check_confirm_password(form):        # checking if the pass is same as confirm_pass
                return render(request,'user_auth/signup.html',{'form':form})

            password = form.cleaned_data['password']
            username = form.cleaned_data['username']

            user.set_password(password)
            user.save()
            user = authenticate(request, username = username, password = password)
            login(request,user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        
        
        form = UserSignupForm()
    return render(request, 'user_auth/signup.html', {'form': form})



def user_login(request):
    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(request.user.profile_picture,type(request.user.profile_picture))
            if user.profile_type == 'patient':
                return redirect('patient_dashboard')
            elif user.profile_type == 'doctor':
                return redirect('doctor_dashboard')
    return render(request, 'user_auth/login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')




@patient_required
def patient_dashboard(request):
    user = request.user
    return render(request, 'user_auth/patient_dashboard.html', {'user': user})
    

@doctor_required
def doctor_dashboard(request):
    user = request.user
    return render(request, 'user_auth/doctor_dashboard.html', {'user': user})