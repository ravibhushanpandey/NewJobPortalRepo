from django.db import models
from datetime import date

# Create your models here.

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        abstract = True

class Contact(Base):
    # cid =models.CharField(max_length=20)
    name = models.CharField(max_length=200,blank=True, null=True)
    email = models.CharField(max_length=200,blank=True, null=True)
    phone = models.CharField(max_length=200,blank=True, null=True)
    msg = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = "contact_info"


class SignUp(Base):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contact = models.CharField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=2000)
    profile_pic = models.FileField(upload_to="images/profile_pic", blank=True, null=True, verbose_name="Profile Image")

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = "signup"

class JobProviderProfile(Base):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200,blank=True, null=True)
    contact = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

class UserProfile1(Base):
    skills = models.CharField(max_length=200,blank=True, null=True)
    experiences = models.CharField(max_length=1000,blank=True, null=True)
    hedline = models.CharField(max_length=200,blank=True, null=True)
    userid = models.ForeignKey(SignUp, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="images", blank=True, null=True, verbose_name="Profile Image")

    # def __str__(self):
    #     return self.skills

    # class Meta:
    #     db_table = "userprofile1"


class Jobs(Base):
    title = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField(max_length=500, blank=True, null=True)
    exp = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False)
    job_pro_user = models.ForeignKey(JobProviderProfile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     db_table = "jobs"


class Apply(Base):
    title = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField(max_length=500, blank=True, null=True)
    exp = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    apdate = models.DateField()
    jobid = models.ForeignKey(Jobs, on_delete=models.CASCADE, blank=True, null=True)
    userid = models.ForeignKey(SignUp, on_delete=models.CASCADE)
    job_pro_user = models.ForeignKey(JobProviderProfile, on_delete=models.CASCADE, blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile1, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     db_table = "applyjob"
