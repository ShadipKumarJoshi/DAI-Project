from django.contrib import admin
from . import models

@admin.register(models.NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_button', 'button_style', 'order', 'is_visible')
    list_editable = ('is_visible', 'order')
    list_filter = ('is_button', 'button_style', 'is_visible')
    search_fields = ('title', 'url')

@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_slide_visible')  # Add the visibility column 
    ordering = ['order']
    list_editable = ('is_slide_visible', 'order')  # O make it editable directly in the list view
    list_filter = ('is_slide_visible',)  #  adds filter sidebar for visibility
