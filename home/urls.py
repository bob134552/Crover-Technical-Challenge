from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("delete/<data_set>", views.delete_data_set, name="delete_data_set")
]