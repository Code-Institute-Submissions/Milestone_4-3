from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.all_properties, name='properties'),
    path('<int:property_id>/', views.property_details, name='property_details'),
    path('add/', views.add_property, name='add_property'),
    path('edit/<int:property_id>', views.edit_property, name='edit_property'),
    path('delete/<int:property_id>', views.delete_property, name='delete_property'),
    path('images/<int:property_id>', views.property_images, name='property_images'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
