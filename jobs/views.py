from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job, JOB_TYPE_CHOICES
from django.contrib import messages

# Create your views here.

@login_required
def job_create(request):
    if not request.user.roles == 'recruiter':
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        print(request.user)
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,'Job Posted Successfully')
            return redirect('recruiter_dashboard')
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostForm()
    
    return render(request,'jobs/jobs_create.html',{'form_data':form})

@login_required
def recruiter_job(request):
    if not request.user.roles == 'recruiter':
        return redirect('student_dashboard')
    
    myjobs = Job.objects.filter(posted_by = request.user).order_by('-created_at') # "-" for descending order
    return render(request,'jobs/recruiter_jobs.html',{'jobs':myjobs})