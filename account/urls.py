from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('login/', views.account_login, name='login'),
    # path('logout/', views.logoutUser, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
    #      form_class=LoginForm, name='login')),

    path('dashboard/',
         views.dashboard, name='dashboard'),
    path('dashboard/edit',
         views.dashboard_edit, name='dashboard_edit'),

    #     path('activate/<slug:uidb64>/<slug:token>/',
    #          views.account_activate, name='activate'),
]
