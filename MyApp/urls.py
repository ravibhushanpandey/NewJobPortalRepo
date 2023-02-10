
from django.urls import path
from . import views, job_provider_view

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('profile_details', views.profile_details),
    path('profile_update/<int:id>', views.profile_update),
    path('profile_insert', views.profile_insert),
    path('signup/<int:id>', views.signup),
    path('apply/<int:id>', views.apply),
    path('update-resume', views.update_resume),

]

urlpatterns_job_provider = [
    path('signup-job-provider', job_provider_view.signup, name='signup_job_provider'),
    path('login-job-provider', job_provider_view.login, name='login_job_provider'),
    path('dashboard-job-provider/<int:id>', job_provider_view.dashboard, name='dashboard_job_provider'),
    path('add-edit-job/<int:jobid>/<int:job_pro_id>', job_provider_view.add_edit_job, name='add_edit_job'),
    path('delete-job/<int:jobid>/<int:job_pro_id>', job_provider_view.delete_job, name='delete_job'),
    path('applied-job/<int:job_pro_id>', job_provider_view.applied_job, name='applied_job'),

]

urlpatterns.extend(urlpatterns_job_provider)
