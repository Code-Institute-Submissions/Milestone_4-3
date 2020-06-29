from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_properties, name='properties'),
    path('<property_id>', views.property_details, name='property_details'),
]
