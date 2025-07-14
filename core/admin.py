from django.contrib import admin
from . import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .forms import NavbarItemForm, CMSPageForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.user import User
from .models import SMEProfile, BDSPProfile

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role', 'business_name', 'pan_vat',
                'full_name', 'mobile',
                'business_registration_number', 'business_type',
            ),
        }),
    )
    list_display = BaseUserAdmin.list_display + ('role',)

admin.site.register(User, UserAdmin)


@admin.register(SMEProfile)
class SMEProfileAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 'user', 'business_size',
        'industry_sector', 'business_stage', 'created_at'
    ]
    search_fields = ['business_name', 'user__username']
    list_filter = ['business_size', 'industry_sector', 'business_stage']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Business Info', {
            'fields': (
                'business_name', 'business_size', 'industry_sector',
                'business_legal_type', 'business_stage', 'ownership_type'
            )
        }),
        ('Service Info', {
            'fields': (
                'service_name', 'service_type',
                'service_description', 'service_logo'
            )
        }),
        ('Documents', {
            'fields': (
                'registration_certificate', 'tax_clearance_certificate'
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
@admin.register(BDSPProfile)
class BDSPProfileAdmin(admin.ModelAdmin):
    list_display = [
        'organization_name', 'user', 'organization_size',
        'industry_sector', 'stage_of_development', 'created_at'
    ]
    search_fields = ['organization_name', 'user__username']
    list_filter = ['organization_size', 'industry_sector', 'stage_of_development']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Organization Info', {
            'fields': (
                'organization_name', 'organization_size', 'industry_sector',
                'legal_type', 'stage_of_development', 'ownership_type'
            )
        }),
        ('Service Info', {
            'fields': (
                'service_name', 'service_type',
                'service_description', 'service_logo'
            )
        }),
        ('Documents', {
            'fields': (
                'business_registration_certificate', 'tax_clearance_certificate'
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
@admin.register(models.NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    form = NavbarItemForm  

    list_display = ('title', 'url', 'is_button', 'button_style', 'order', 'is_active')
    list_editable = ('is_active', 'order')
    list_filter = ('is_button', 'button_style', 'is_active')
    search_fields = ('title', 'url')

@admin.register(models.HeroCarousel)
class HeroCarouselAdmin(admin.ModelAdmin):
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

@admin.register(models.ServiceTag)
class ServiceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(models.ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    # fields = ('title', 'description', 'tags', 'order', 'is_active', 'image')

@admin.register(models.SMEGuidelineCard)
class SMEGuidelineCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
@admin.register(models.NewsEventType)
class NewsEventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.NewsEventStatus)
class NewsEventStatusAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'location', 'type', 'status_tag', 'is_featured', 'is_active', 
        'publication_start', 'publication_end', 'created_at', 'updated_at'
    ]
    list_filter = ['is_active', 'is_featured', 'type', 'status_tag']
    list_editable = ('is_featured', 'is_active')
    search_fields = ['title', 'description', 'location']
    ordering = ['-created_at']
    
@admin.register(models.FooterQuickLink)
class FooterQuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

@admin.register(models.FooterContactInfo)
class FooterContactInfoAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

@admin.register(models.FooterSocialMedia)
class FooterSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
class NoticeAttachmentInline(admin.TabularInline):
    model = models.NoticeAttachment
    extra = 1  # How many empty forms to show by default

@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'pop_up')
    inlines = [NoticeAttachmentInline]
    list_editable = ('pop_up',)
 
class CMSPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = models.CMSPage
        fields = '__all__'
   
@admin.register(models.CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    form =  CMSPageForm
    list_display = ('title', 'slug', 'published', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')


