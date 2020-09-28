from django.urls import path
from django.contrib.auth import views as d_views

from accounts import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('registerStudent/', views.register_worker_view, name='registerStudent'),
    path('registerManager/', views.register_manager_view, name='registerManager'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('userDetail/', views.WorkerDetailView.as_view(), name='detail')
]

app_name = 'accounts'
