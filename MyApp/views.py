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

# Create your views here.


def loginUser(request):

    if request.session.has_key('logged_in'):
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        # user = authenticate(username=username, password=password)
        users = SignUp.objects.all()
        for user in users:
            if user.username == username and user.password == password:
                # store session
                login = request.session['logged_in'] = True
                # session expiry if value=0 the it will expire the session while closing the browser as well as while trying on diffrent browser
                request.session.set_expiry(0)
                username = request.session['username'] = user.username
                request.session['userid'] = user.id

                userid = request.session.get('userid')
                jobid = request.session.get('jobid')
                jobs = Jobs.objects.all()
                signup = SignUp.objects.filter(id=userid)
                hedlines = UserProfile1.objects.filter(userid=userid)
                applies = Apply.objects.filter(userid=userid)
                appliescount = Apply.objects.filter(userid=userid).count()

                ap = []
                for applied in applies:
                    ap.append(applied.jobid_id)
                jobs = Jobs.objects.filter(status=True).exclude(id__in=ap)
                jobscount = jobs.exclude(id__in=ap).count()
                return render(request, 'index.html', {'jobscount': jobscount, 'appliescount': appliescount, 'login': login, 'username': username, 'jobs': jobs, 'signup': signup, 'hedlines': hedlines, 'applies': applies})

        errorcheck = "User or Password is Wrong !!"
        return render(request, 'login.html', {'error': errorcheck})

    return render(request, 'login.html')


def index(request):

    login = request.session.get('logged_in')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
        messages.success(request, 'Your message has been sent!')

    username = request.session.get('username')
    userid = request.session.get('userid')
    print(username)
    jobid = request.session.get('jobid')
    # jobs = Jobs.objects.all()
    signup = SignUp.objects.filter(id=userid)
    hedlines = UserProfile1.objects.filter(userid=userid)
    applies = Apply.objects.filter(userid=userid)
    appliescount = Apply.objects.filter(userid=userid).count()

    ap = []
    for applied in applies:
        ap.append(applied.jobid.id)
    jobs = Jobs.objects.filter(status=True).exclude(id__in=ap)
    jobscount = jobs.count()
    # jobs = Jobs.objects.exclude(
    # reduce(operator.and_, (Q(id__in=x) for x in ap)))
    print(jobs)
    context = {'username': username,
               'login': login,
               'jobs': jobs,
               'signup': signup,
               'hedlines': hedlines,
               'applies': applies,
               'appliescount': appliescount,
               'jobscount': jobscount
               }
    return render(request, "index.html", context)


def logoutUser(request):
    logout(request)
    try:
        del request.session['logged_in']
    except KeyError:
        pass
    return redirect("/login")


def profile_insert(request):  # page not connected to the index.html page

    if request.method == "POST":
        userid = request.session.get('userid')
        skills = request.POST.get('skills')
        exp = request.POST.get('exp')
        hedline = request.POST.get('hedline')
        profile = UserProfile1(
            skills=skills, experiences=exp, hedline=hedline, userid_id=userid)
        profile.save()
        return redirect("/profile_details")
    return render(request, "profile_insert.html")


def profile_update(request, id):
    userid = request.session.get('userid')
    profiles = UserProfile1.objects.filter(
        userid=userid)
    print(profiles)

    if request.method == "POST":
        print("hello akash")
        proid = UserProfile1.objects.get(id=id)
        print(proid)
        form = ProfileUpdateForm(request.POST, instance=proid)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect("/profile_details")

        return redirect("/profile_details")
    return render(request, "profile_update.html", {'profiles': profiles})


def profile_details(request):  # page not connected to the index.html page
    userid = request.session.get('userid')
    # profile_fill = request.session.get('profile_fill')
    # username = request.session.get('username')
    signup = SignUp.objects.filter(id=userid)
    print(signup)
    profiles = UserProfile1.objects.filter(userid=userid)
    user_resume = UserProfile1.objects.filter(userid=userid).first()
    # print("user_resume ",user_resume.resume)
    count = UserProfile1.objects.filter(userid=userid).count()
    if count == 0:
        print("profile false")
        messages.success(request, 'Update Your Profile')

    # print(profiles)
    context = {
        "count": count,
        "profiles": profiles,
        "signup": signup,
        "user_resume":user_resume
    }
    if count > 0:
        return render(request, "profile_details.html", context)

    return render(request, "profile_details.html", context)


def signup(request,id):
    print("hello.")
    if not id:
        signup_obj = None
    else:
        signup_obj = SignUp.objects.filter(pk=id).first()

    if request.method == "POST":
        if not id:
            form = SignUpForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                return redirect("/login")
        else:
            signup_obj = SignUp.objects.filter(pk=id).first()
            try:
                profile_pic = request.FILES["profile_pic"]
                signup_obj.profile_pic = profile_pic
            except:
                pass
            signup_obj.name = request.POST.get("name")
            signup_obj.email = request.POST.get("email")
            signup_obj.contact = request.POST.get("contact")
            signup_obj.location = request.POST.get("location")
            signup_obj.save()
            return redirect("/profile_details")



    return render(request, "signup.html",locals())


def apply(request, id):
    if request.session.has_key('logged_in') == False:
        return redirect("/login")

    userid = request.session.get('userid')
    profiles = UserProfile1.objects.filter(userid=userid).first()
    if not profiles:
        # request.session['profile_fill'] = False
        return redirect("/profile_details")

    apdate = date.today()
    userid = request.session.get('userid')
    request.session['jobid'] = id
    apply = Jobs.objects.filter(id=id)
    for apjob in apply:
        title = apjob.title
        details = apjob.details
        exp = apjob.exp
        jobid = apjob
        job_pro_id = apjob.job_pro_user_id

    applied = Apply(title=title, details=details,
                    exp=exp, apdate=apdate, jobid=jobid, user_profile=profiles, userid_id=userid, job_pro_user_id=job_pro_id)
    applied.save()
    return redirect("/#section3")
    # return render(request, "index.html")

def update_resume(request):
    userid = request.session.get('userid')
    profiles = UserProfile1.objects.filter(
        userid__id=userid).first()
    print(profiles)

    if not profiles:
        profiles = UserProfile1()
    try:
        resume_file = request.FILES['resume']
        is_file = True
    except:
        is_file = False

    if request.method == "POST" and is_file == True:
        profiles.resume = resume_file
        profiles.userid_id = userid
        profiles.save()

    return redirect("/profile_details")

