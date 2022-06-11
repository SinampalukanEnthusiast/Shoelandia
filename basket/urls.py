from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.basket_summary, name="basket_summary")
]
