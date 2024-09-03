from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_to_csv_view, name='pdf_to_csv'),
]
