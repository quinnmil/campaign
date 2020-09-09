from django.urls import path

from gigs.views import JobsList, DetailView, claim_job

urlpatterns = [
    path('', JobsList.as_view(), name='jobsList'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('claim', claim_job, name='claim')
]

app_name = 'gigs'
