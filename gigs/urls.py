from django.urls import path

from gigs.views import index, JobsList, DetailView

urlpatterns = [
    path('', index, name='index'),
    path('jobs/', JobsList.as_view(), name='jobsList'),
    path('<int:pk>', DetailView.as_view(), name='detail')
]

app_name = 'gigs'
