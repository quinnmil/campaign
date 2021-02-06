"""gigs urls"""
from django.urls import path, reverse_lazy

from django.contrib.auth.decorators import login_required
from gigs.views import JobsList, DetailView, claim_job, quit_job
from management import views as ManagementViews

ACCOUNT_LOGIN = 'accounts:login'

urlpatterns = [
    path('',
         login_required(JobsList.as_view(),
                        login_url=reverse_lazy(ACCOUNT_LOGIN)), name='list'),
    path('<int:pk>',
         login_required(DetailView.as_view(),
                        login_url=reverse_lazy(ACCOUNT_LOGIN)), name='detail'),
    path('claim',
         login_required(
             claim_job, login_url=reverse_lazy(ACCOUNT_LOGIN)), name='claim'),
    path('<int:job_id>/complete',
         login_required(ManagementViews.complete_job,
                        login_url=reverse_lazy(ACCOUNT_LOGIN)), name='complete'),
    path('quit',
         login_required(quit_job, login_url=reverse_lazy(ACCOUNT_LOGIN)), name='quit')
]

app_name = 'gigs'
