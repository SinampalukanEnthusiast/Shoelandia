from django.urls import path
from . import views

#app_name = 'store'

urlpatterns = [
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    #path('register/', views.register, name="register"),
    #path('cart/', views.cart, name="cart"),
    #path('checkout/', views.checkout, name="checkout"),
    #path('update_item/', views.update_item, name="update_item"),
    #path('process_order/', views.process_order, name="process_order"),
    path('<slug:slug>', views.product_detail, name="product_detail"),

]
