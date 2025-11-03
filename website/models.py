from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import EmailValidator
import json


class Contact(models.Model):
    """Modèle pour les messages de contact"""
    
    STATUS_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('lu', 'Lu'),
        ('repondu', 'Répondu'),
        ('traite', 'Traité'),
    ]
    
    SERVICE_CHOICES = [
        ('azi_group', 'AZI GROUP'),
        ('gss', 'Global Songhoy Services (GSS)'),
        ('sogis', 'Sogis - Immobilier'),
        ('golden', 'Société Golden - Transport'),
        ('angnie', 'Angnie Mali - Propreté'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name="Entreprise/Organisation")
    service = models.CharField(
        max_length=10, 
        choices=SERVICE_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="Service concerné"
    )
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='nouveau', 
        verbose_name="Statut"
    )
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def get_absolute_url(self):
        return reverse('admin:website_contact_change', args=[str(self.id)])


class Company(models.Model):
    """Modèle pour les entreprises du groupe"""
    
    name = models.CharField(max_length=100, verbose_name="Nom de l'entreprise")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description courte")
    detailed_description = models.TextField(
        blank=True, 
        verbose_name="Description détaillée",
        help_text="Description complète des domaines clés et KPI"
    )
    icon = models.CharField(max_length=10, verbose_name="Icône (emoji)")
    logo = models.ImageField(
        upload_to='company_logos/', 
        blank=True, 
        null=True, 
        verbose_name="Logo de l'entreprise"
    )
    gradient = models.CharField(
        max_length=200, 
        default="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        verbose_name="Dégradé CSS"
    )
    services = models.JSONField(
        default=list,
        verbose_name="Services (JSON)",
        help_text="Liste des services au format JSON"
    )
    kpis = models.JSONField(
        default=list,
        verbose_name="KPI (JSON)",
        help_text="Liste des KPI au format JSON"
    )
    active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('website:company_detail', args=[str(self.slug)])
    
    def get_services_list(self):
        """Retourne la liste des services"""
        if isinstance(self.services, list):
            return self.services
        try:
            return json.loads(self.services)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def get_kpis_list(self):
        """Retourne la liste des KPI"""
        if isinstance(self.kpis, list):
            return self.kpis
        try:
            return json.loads(self.kpis)
        except (json.JSONDecodeError, TypeError):
            return []


class CompanyProjectImage(models.Model):
    """Modèle pour les images de projets des entreprises"""
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='project_images',
        verbose_name="Entreprise"
    )
    image = models.ImageField(
        upload_to='company_projects/', 
        verbose_name="Image du projet"
    )
    title = models.CharField(
        max_length=200, 
        verbose_name="Titre du projet",
        help_text="Nom ou description du projet"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Description du projet"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Image de projet"
        verbose_name_plural = "Images de projets"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.title}"


class News(models.Model):
    """Modèle pour les actualités"""
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Contenu")
    excerpt = models.TextField(
        max_length=300, 
        blank=True, 
        verbose_name="Extrait",
        help_text="Court résumé de l'article (optionnel)"
    )
    image = models.ImageField(
        upload_to='news/', 
        blank=True, 
        null=True, 
        verbose_name="Image"
    )
    image_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="URL de l'image",
        help_text="Alternative à l'upload d'image"
    )
    published = models.BooleanField(default=True, verbose_name="Publié")
    featured = models.BooleanField(default=False, verbose_name="Article en vedette")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('website:news_detail', args=[str(self.slug)])
    
    def get_excerpt(self):
        """Retourne l'extrait ou les 150 premiers caractères du contenu"""
        if self.excerpt:
            return self.excerpt
        return self.content[:150] + "..." if len(self.content) > 150 else self.content
    
    def get_image_url(self):
        """Retourne l'URL de l'image (upload ou URL externe)"""
        if self.image:
            return self.image.url
        return self.image_url


class Setting(models.Model):
    """Modèle pour les paramètres du site"""
    
    key = models.CharField(max_length=100, unique=True, verbose_name="Clé")
    value = models.TextField(verbose_name="Valeur")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Récupère un paramètre par sa clé"""
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_setting(cls, key, value, description=""):
        """Définit un paramètre"""
        setting, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            setting.value = value
            setting.description = description
            setting.save()
        return setting


class Testimonial(models.Model):
    """Modèle pour les témoignages clients"""
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    company = models.CharField(max_length=100, verbose_name="Entreprise")
    position = models.CharField(max_length=100, blank=True, verbose_name="Poste")
    content = models.TextField(verbose_name="Témoignage")
    image = models.ImageField(
        upload_to='testimonials/', 
        blank=True, 
        null=True, 
        verbose_name="Photo"
    )
    rating = models.IntegerField(
        default=5, 
        verbose_name="Note",
        help_text="Note de 1 à 5 étoiles"
    )
    active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    def get_stars(self):
        """Retourne le nombre d'étoiles pour l'affichage"""
        return "★" * self.rating + "☆" * (5 - self.rating)


class NavigationLogo(models.Model):
    """Modèle pour le logo de navigation programmable"""
    
    name = models.CharField(
        max_length=100, 
        default="AZI GROUP",
        verbose_name="Nom de l'entreprise"
    )
    logo = models.ImageField(
        upload_to='navigation/', 
        verbose_name="Logo de navigation",
        help_text="Logo qui apparaîtra dans la barre de navigation"
    )
    active = models.BooleanField(
        default=True, 
        verbose_name="Actif",
        help_text="Désactiver pour masquer ce logo"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Logo de navigation"
        verbose_name_plural = "Logos de navigation"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Logo navigation - {self.name}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'un seul logo de navigation actif
        if self.active:
            NavigationLogo.objects.filter(active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_logo(cls):
        """Retourne le logo de navigation actif"""
        try:
            return cls.objects.get(active=True)
        except cls.DoesNotExist:
            return None


class HomePageHero(models.Model):
    """Modèle pour la section hero de la page d'accueil"""
    
    title = models.CharField(
        max_length=200, 
        default="AZI GROUP",
        verbose_name="Titre principal"
    )
    subtitle = models.TextField(
        default="Excellence Opérationnelle au Service de l'Impact en Afrique de l'Ouest",
        verbose_name="Sous-titre"
    )
    background_image = models.ImageField(
        upload_to='homepage/', 
        verbose_name="Image de fond",
        help_text="Image qui apparaîtra en arrière-plan de la section hero"
    )
    overlay_opacity = models.FloatField(
        default=0.5,
        verbose_name="Opacité de l'overlay",
        help_text="Valeur entre 0 (transparent) et 1 (opaque)"
    )
    active = models.BooleanField(
        default=True, 
        verbose_name="Actif",
        help_text="Désactiver pour masquer cette section"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Section Hero de la page d'accueil"
        verbose_name_plural = "Sections Hero de la page d'accueil"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Hero - {self.title}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule section hero active
        if self.active:
            HomePageHero.objects.filter(active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_hero(cls):
        """Retourne la section hero active"""
        try:
            return cls.objects.get(active=True)
        except cls.DoesNotExist:
            return None