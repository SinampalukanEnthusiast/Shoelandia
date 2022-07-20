from xml.etree.ElementInclude import include
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('login/', views.account_login, name='login'),
    # path('logout/', views.logoutUser, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
    #      form_class=LoginForm, name='login')),
    path('dashboard/',
         views.dashboard, name='dashboard'),
    path('dashboard/edit/',
         views.dashboard_edit, name='dashboard_edit'),
    path('dashboard/delete_user/',
         views.delete_user, name='delete_user'),
    path('dashboard/delete_user/confirm/',
         TemplateView.as_view(template_name="account/user/delete_confirm.html"), name='delete_confirm'),
    path('dashboard/orders/',
         views.orders, name='orders'),
    path('dashboard/orders/<slug:id>',
         views.order_detail, name='order_detail'),
    path('dashboard/orders/return/<str:pk>',
         views.return_order, name='return_order'),
    path('addresses/',
         views.addresses, name='addresses'),
    path('addresses/add/',
         views.add_address, name='add_address'),
    path('addresses/edit/<slug:id>',
         views.edit_address, name='edit_address'),
    path('addresses/delete/<slug:id>',
         views.delete_address, name='delete_address'),
    path('addresses/set_default/<slug:id>',
         views.set_default, name='set_default'),
]
