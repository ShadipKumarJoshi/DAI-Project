from django.contrib import admin
from . import models


@admin.register(models.NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_button',
                    'button_style', 'order', 'is_active')
    list_editable = ('is_active', 'order')
    list_filter = ('is_button', 'button_style', 'is_active')
    search_fields = ('title', 'url')


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    # Add the visibility column
    list_display = ('title', 'order', 'is_slide_active')
    ordering = ['order']
    # O make it editable directly in the list view
    list_editable = ('is_slide_active', 'order')
    list_filter = ('is_slide_active',)  # adds filter sidebar for visibility


class SMEDevelopmentStepInline(admin.TabularInline):
    model = models.SMEDevelopmentStep
    extra = 0
    min_num = 4
    max_num = 4


@admin.register(models.SMEDevelopmentStepSection)
class SMEDevelopmentStepSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    inlines = [SMEDevelopmentStepInline]


@admin.register(models.SMEDevelopmentStep)
class SMEDevelopmentStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'section')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'section')
    ordering = ['section', 'order']
