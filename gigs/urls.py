from django.urls import path

from gigs.views import index, JobsList

urlpatterns = [
    path('', index, name='index'),
    path('jobs/', JobsList.as_view())
]