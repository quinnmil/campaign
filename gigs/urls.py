from django.urls import path

from gigs.views import JobsList, DetailView, claim_job, quit_job

urlpatterns = [
    path('', JobsList.as_view(), name='list'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('claim', claim_job, name='claim'),
    path('quit', quit_job, name='quit')
]

app_name = 'gigs'
