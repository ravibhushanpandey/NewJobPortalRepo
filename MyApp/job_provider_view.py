from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.db import connection
from .forms import ContactForm, ProfileUpdateForm, SignUpForm
from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import Length, Upper, Lower
from django.contrib.sessions.models import Session
# from django_globals import globals
from datetime import date
from functools import reduce
import operator

from .models import JobProviderProfile,Jobs
from django.urls import reverse

# Create your views here.

def login(request):

    if request.method == 'POST':
        uname = request.POST.get("uname")
        psw = request.POST.get("psw")

        job_profile_obj = JobProviderProfile.objects.filter(
            username=uname,
            password=psw
        ).first()
        print("job_profile_obj ",job_profile_obj)
        if job_profile_obj:
            return redirect(f'dashboard-job-provider/{job_profile_obj.pk}')

    return render(request, 'job_provider/login.html',locals())

def signup(request):

    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        psw = request.POST.get("psw")
        contact = request.POST.get("contact")

        job_profile_obj = JobProviderProfile.objects.create(
            name=name,
            email=email,
            username=username,
            password=psw,
            contact=contact
        )
        redirect("login-job-provider")

    return render(request, 'job_provider/signup.html')

def dashboard(request,id):
    jobs_obj = Jobs.objects.filter(job_pro_user_id=id).order_by('-pk')

    return render(request, 'job_provider/dashboard.html',locals())

def add_edit_job(request,jobid,job_pro_id):

    if jobid != 0:
        jobs_obj = Jobs.objects.filter(pk=jobid).first()
    else:
        print("else")
        jobs_obj = Jobs()

    if request.method == "POST":
        jobs_obj.title = request.POST.get("title")
        jobs_obj.exp = request.POST.get("exp")
        jobs_obj.company = request.POST.get("company")
        jobs_obj.location = request.POST.get("location")
        jobs_obj.status = request.POST.get("status")
        jobs_obj.details = request.POST.get("details")
        jobs_obj.job_pro_user_id = job_pro_id
        jobs_obj.save()
        return redirect(f"/dashboard-job-provider/{jobs_obj.job_pro_user.pk}")

    return render(request, 'job_provider/add_edit_job.html',locals())

def delete_job(request,jobid,job_pro_id):

    jobs_obj = Jobs.objects.filter(pk=jobid).first()
    jobs_obj.delete()

    return redirect(f"/dashboard-job-provider/{jobs_obj.job_pro_user.pk}")

def applied_job(request,job_pro_id):

    applied_jobs_obj = Apply.objects.filter(job_pro_user_id=job_pro_id)

    return render(request, 'job_provider/applied_jobs.html',locals())