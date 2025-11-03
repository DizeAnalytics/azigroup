from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Company, CompanyProjectImage, News, Setting, Testimonial, HomePageHero, NavigationLogo


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'service', 'status', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['name', 'email', 'company', 'message']
    readonly_fields = ['created_at']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message', {
            'fields': ('service', 'message')
        }),
        ('Gestion', {
            'fields': ('status', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


class CompanyProjectImageInline(admin.TabularInline):
    model = CompanyProjectImage
    extra = 0
    fields = ('image', 'title', 'description', 'order')
    ordering = ['order']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['name', 'description', 'detailed_description']
    list_editable = ['active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CompanyProjectImageInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'slug', 'description', 'detailed_description', 'icon', 'logo')
        }),
        ('Apparence', {
            'fields': ('gradient',)
        }),
        ('Contenu', {
            'fields': ('services', 'kpis'),
            'description': 'Utilisez le format JSON pour les listes'
        }),
        ('Statut', {
            'fields': ('active',)
        }),
    )
    
    def get_services_list(self, obj):
        return obj.get_services_list()
    get_services_list.short_description = 'Services'


@admin.register(CompanyProjectImage)
class CompanyProjectImageAdmin(admin.ModelAdmin):
    list_display = ['company', 'title', 'order', 'created_at']
    list_filter = ['company', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    list_editable = ['order']
    ordering = ['company', 'order']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'featured', 'created_at']
    list_filter = ['published', 'featured', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    list_editable = ['published', 'featured']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Image', {
            'fields': ('image', 'image_url'),
            'description': 'Vous pouvez soit uploader une image soit fournir une URL'
        }),
        ('Publication', {
            'fields': ('published', 'featured')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview', 'description_preview']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def value_preview(self, obj):
        return obj.value[:50] + "..." if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Valeur'
    
    def description_preview(self, obj):
        return obj.description[:30] + "..." if len(obj.description) > 30 else obj.description
    description_preview.short_description = 'Description'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'active', 'created_at']
    list_filter = ['active', 'rating', 'created_at']
    search_fields = ['name', 'company', 'content']
    list_editable = ['active', 'rating']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('name', 'company', 'position', 'image')
        }),
        ('Témoignage', {
            'fields': ('content', 'rating')
        }),
        ('Statut', {
            'fields': ('active',)
        }),
    )


@admin.register(NavigationLogo)
class NavigationLogoAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['name']
    list_editable = ['active']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'logo')
        }),
        ('Statut', {
            'fields': ('active',),
            'description': 'Une seule logo de navigation peut être active à la fois'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    def has_add_permission(self, request):
        # Limiter à une seule logo de navigation active
        if NavigationLogo.objects.filter(active=True).exists():
            return False
        return True


@admin.register(HomePageHero)
class HomePageHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'overlay_opacity', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['active']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'subtitle')
        }),
        ('Image de fond', {
            'fields': ('background_image', 'overlay_opacity'),
            'description': 'L\'opacité de l\'overlay contrôle la transparence du texte sur l\'image'
        }),
        ('Statut', {
            'fields': ('active',),
            'description': 'Une seule section hero peut être active à la fois'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    def has_add_permission(self, request):
        # Limiter à une seule section hero active
        if HomePageHero.objects.filter(active=True).exists():
            return False
        return True


# Configuration de l'interface d'administration
admin.site.site_header = "AZI GROUP - Administration"
admin.site.site_title = "AZI GROUP Admin"
admin.site.index_title = "Tableau de bord"