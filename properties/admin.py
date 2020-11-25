from django.contrib import admin
from .models import Category, Feature, Image, Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('short_description', 'category', 'daily_price', 'owner')
    ordering = ('category', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feature)
admin.site.register(Image)
