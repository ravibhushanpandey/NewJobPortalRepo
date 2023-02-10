from django.contrib import admin

# Register your models here.
from .models import Contact,Jobs,UserProfile1,SignUp,Apply,JobProviderProfile

admin.site.register(Contact)
admin.site.register(Jobs)
admin.site.register(UserProfile1)
admin.site.register(SignUp)
admin.site.register(Apply)
admin.site.register(JobProviderProfile)

