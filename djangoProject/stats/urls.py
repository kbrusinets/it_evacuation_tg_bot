from django.urls import path
from . import views

urlpatterns = [
    path('population/', views.say_hello)
]
