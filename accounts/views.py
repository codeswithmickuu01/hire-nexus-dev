from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import StudentSignUpForm, RecruiterSignUpForm
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required

# Create your views here.

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES) # files for image upload
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Student account created successfully.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type':'Student'})



def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST, request.FILES) # files for image upload
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Recruiter account created successfully.")
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterSignUpForm()
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type':'Recruiter'})


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request,username=user_obj.email,password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request,user)
            if user.roles == 'student':
                messages.success(request, "Logged in successfully as Student.")
                return redirect('student_dashboard')
            elif user.roles == 'recruiter':
                messages.success(request, "Logged in successfully as Recruiter.")
                return redirect('recruiter_dashboard')
            else:
                return redirect('admin:index')
            
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')

@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

@login_required
def recruiter_dashboard(request):
    return render(request, 'accounts/recruiter_dashboard.html')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')