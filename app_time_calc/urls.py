from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="Main"),
    path('confirm/', views.confirm, name="Confirm"),
]
