from django.urls import path
from facturaciononline import views

urlpatterns = [
    path('', views.consulta),
]
