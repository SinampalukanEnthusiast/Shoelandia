from django.urls import path
from . import views

#app_name = 'store'

urlpatterns = [
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('store/<slug:slug>/', views.product_detail, name="product_detail"),
    path('category/<slug:category>/',
         views.category_products, name="category_products"),

]
