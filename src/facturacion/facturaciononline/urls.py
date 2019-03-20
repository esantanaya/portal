from django.urls import path
from facturaciononline import views

urlpatterns = [
    path('', views.consulta_carga),
    path('consulta/', views.consulta),
    path('timbre/', views.timbre),
    path('zipper/', views.zipper),
]
