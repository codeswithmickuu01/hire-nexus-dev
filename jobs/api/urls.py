from django.urls import path
from .views import job_list,job_detail,create_job_api,apply_job_api,my_application_api,job_application_recruiter_api,update_application_status_api


urlpatterns = [
    path('job_listing/',job_list,name='job_listing'),
    path('job_detail/<int:id>/',job_detail,name='job_detail'),
    path('job_create/',create_job_api,name='job_create'),
    path('jobs/_apply/',apply_job_api,name='job_create'),
    path('my_application/',my_application_api,name='my_applications'),
    path('view_applicant/<int:job_id>/',job_application_recruiter_api,name='job_applicant_recruiter_api'),
    path('application/int:application_id>/status',update_application_status_api,name='update_status')


]


