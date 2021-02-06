from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('registerStudent/', views.register_worker_view, name='registerStudent'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('userDetail/', views.WorkerDetailView.as_view(), name='detail')
    # path('registerManager/', views.register_manager_view, name='registerManager'),
]

app_name = 'accounts'
