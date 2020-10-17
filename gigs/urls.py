from django.urls import path, reverse_lazy

from django.contrib.auth.decorators import login_required
from gigs.views import JobsList, DetailView, claim_job, quit_job
from management import views as ManagementViews

urlpatterns = [
    path('', JobsList.as_view(), name='list'),
    path('<int:pk>', login_required(DetailView.as_view(),
                                    login_url=reverse_lazy('accounts:login')), name='detail'),
    path('claim', login_required(
        claim_job, login_url=reverse_lazy('accounts:login')), name='claim'),
    path('<int:job_id>/complete',
         login_required(ManagementViews.complete_job,
                        login_url=reverse_lazy('accounts:login')), name='complete'),
    path('quit', login_required(
        quit_job, login_url=reverse_lazy('accounts:login')), name='quit')
]

app_name = 'gigs'
