from django.urls import path

from gigs.views import index, JobsList, DetailView, claimJob

urlpatterns = [
    path('', JobsList.as_view(), name='jobsList'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('claim', claimJob, name='claim')
]

app_name = 'gigs'
