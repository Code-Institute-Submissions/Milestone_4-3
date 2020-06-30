from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_properties, name='properties'),
    path('<int:property_id>/', views.property_details, name='property_details'),
    path('add/', views.add_property, name='add_property'),
]
