from django.urls import path
from django.contrib.auth import views as d_views

from accounts import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'), 
    path('registerStudent/', views.register_worker_view, name='registerStudent'),
    path('registerManager/', views.register_manager_view, name='registerManager'),
    path('login/', d_views.LoginView.as_view(), name='login'),
]

app_name = 'accounts'

# from django.contrib.auth.urls 