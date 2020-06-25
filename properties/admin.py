from django.contrib import admin
from .models import Category, Feature, Image, Property

# Register your models here.
admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Feature)
admin.site.register(Image)