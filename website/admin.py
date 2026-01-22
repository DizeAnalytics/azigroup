from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Company, CompanyProjectImage, News, NewsImage, Setting, Testimonial, HomePageHero, HomePageSlide, NavigationLogo, Project, ProjectImage, ContactInfo, UserProfile, Visitor, AboutSectionImage


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


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ['order']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'featured', 'created_at']
    list_filter = ['published', 'featured', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    list_editable = ['published', 'featured']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [NewsImageInline]
    
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
    list_display = ['name', 'logo_preview', 'active', 'created_at', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['name']
    list_editable = ['active']
    readonly_fields = ['logo_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'logo', 'logo_preview')
        }),
        ('Statut', {
            'fields': ('active',),
            'description': 'Un seul logo de navigation peut être actif à la fois. Quand vous activez ce logo, les autres seront automatiquement désactivés.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        """Affiche un aperçu du logo dans l'admin"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 200px; object-fit: contain;" />',
                obj.logo.url
            )
        return "Aucun logo"
    logo_preview.short_description = 'Aperçu du logo'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


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


@admin.register(HomePageSlide)
class HomePageSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order', 'overlay_opacity', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'subtitle', 'button_text', 'button_url']
    list_editable = ['active', 'order']
    ordering = ['order', '-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'subtitle')
        }),
        ('Média', {
            'fields': ('image', 'overlay_opacity')
        }),
        ('Bouton (optionnel)', {
            'fields': ('button_text', 'button_url')
        }),
        ('Affichage', {
            'fields': ('active', 'order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AboutSectionImage)
class AboutSectionImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'active', 'created_at', 'updated_at']
    list_filter = ['active', 'created_at']
    list_editable = ['active']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Photo', {
            'fields': ('image', 'image_preview'),
            'description': 'Photo qui s\'affichera dans la section "Qui Sommes-Nous ?" de la page d\'accueil. Format carré recommandé pour un meilleur rendu.'
        }),
        ('Statut', {
            'fields': ('active',),
            'description': 'Une seule photo peut être active à la fois. Quand vous activez cette photo, les autres seront automatiquement désactivées.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Affiche un aperçu de la photo dans l'admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 50%; border: 4px solid #E45B40; object-fit: cover;" />',
                obj.image.url
            )
        return "Aucune photo"
    image_preview.short_description = 'Aperçu'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ['order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_partners', 'status', 'start_date', 'completion_date', 'created_at']
    list_filter = ['status', 'partners', 'created_at']
    search_fields = ['title', 'description', 'client', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'slug', 'partners', 'status', 'client', 'location')
        }),
        ('Détails', {
            'fields': ('description', 'contract_details', 'duration')
        }),
        ('Dates', {
            'fields': ('start_date', 'completion_date', 'completion_info')
        }),
        ('Média', {
            'fields': ('image',)
        }),
    )

    def get_partners(self, obj):
        return ", ".join([p.name for p in obj.partners.all()])
    get_partners.short_description = 'Partenaires'


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'active', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['email', 'phone', 'address']
    list_editable = ['active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de contact', {
            'fields': ('address', 'address_details', 'email', 'phone', 'hours')
        }),
        ('Statut', {
            'fields': ('active',),
            'description': 'Une seule information de contact peut être active à la fois. Quand vous activez cette information, les autres seront automatiquement désactivées.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_full_name', 'country', 'phone', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'first_name', 'last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',)
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'country', 'phone')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nom complet'


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'path', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ip_address', 'path', 'user_agent']
    readonly_fields = ['ip_address', 'user_agent', 'path', 'referer', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de visite', {
            'fields': ('ip_address', 'path', 'referer', 'user_agent')
        }),
        ('Date', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Les visiteurs sont créés automatiquement
    
    def has_change_permission(self, request, obj=None):
        return False  # Les visiteurs ne peuvent pas être modifiés
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


# Configuration de l'interface d'administration
admin.site.site_header = "IBC Sarl BTP - Administration"
admin.site.site_title = "IBC Sarl BTP Admin"
admin.site.index_title = "Tableau de bord"
