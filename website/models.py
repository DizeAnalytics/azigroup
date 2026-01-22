from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        ('azi_group', 'IBC SARL BTP'),
        ('gss', 'Global Songhoy Services (GSS)'),
        ('sogis', 'Sogis - Immobilier'),
        ('golden', 'Société Golden - Transport'),
        ('angnie', 'Angnie Mali - Propreté'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name="Téléphone")
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


class NewsImage(models.Model):
    """Modèle pour les images additionnelles des actualités"""
    
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Actualité"
    )
    image = models.ImageField(
        upload_to='news/gallery/', 
        verbose_name="Image"
    )
    caption = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Légende"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image pour {self.news.title}"


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
        default="IBC Sarl BTP",
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
        default="IBC Sarl BTP",
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


class HomePageSlide(models.Model):
    """Modèle pour les slides du carrousel de la page d'accueil"""

    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.TextField(blank=True, verbose_name="Sous-titre")
    image = models.ImageField(
        upload_to='homepage/slides/',
        verbose_name="Image",
        help_text="Image de fond du slide (format large recommandé)"
    )
    overlay_opacity = models.FloatField(
        default=0.45,
        verbose_name="Opacité de l'overlay",
        help_text="Valeur entre 0 (transparent) et 1 (opaque)"
    )
    button_text = models.CharField(max_length=60, blank=True, verbose_name="Texte du bouton")
    button_url = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Lien du bouton",
        help_text="Ex: /projects/ ou https://..."
    )
    active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Slide d'accueil"
        verbose_name_plural = "Slides d'accueil"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Slide #{self.order} - {self.title}"


class AboutSectionImage(models.Model):
    """Modèle pour la photo de la section 'Qui Sommes-Nous ?' de la page d'accueil"""
    
    image = models.ImageField(
        upload_to='homepage/about/',
        verbose_name="Photo",
        help_text="Photo qui s'affichera dans la section 'Qui Sommes-Nous ?' (format carré recommandé)"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Désactiver pour masquer cette photo"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Photo 'Qui Sommes-Nous ?'"
        verbose_name_plural = "Photos 'Qui Sommes-Nous ?'"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Photo Qui Sommes-Nous - {self.created_at.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule photo active
        if self.active:
            AboutSectionImage.objects.filter(active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_image(cls):
        """Retourne la photo active de la section 'Qui Sommes-Nous ?'"""
        try:
            return cls.objects.get(active=True)
        except cls.DoesNotExist:
            return None


class Project(models.Model):
    """Modèle pour les projets réalisés et en cours"""
    
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('realise', 'Réalisé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre du projet")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    partners = models.ManyToManyField(
        Company, 
        related_name='projects',
        verbose_name="Partenaires",
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='en_cours', 
        verbose_name="Statut"
    )
    description = models.TextField(verbose_name="Description détaillée")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    contract_details = models.TextField(blank=True, verbose_name="Ensemble de contrats")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Durée d'exécution")
    start_date = models.DateField(blank=True, null=True, verbose_name="Date de début")
    completion_date = models.DateField(blank=True, null=True, verbose_name="Date de fin / Livraison")
    completion_info = models.TextField(blank=True, verbose_name="Info sur la fin de réalisation")
    image = models.ImageField(
        upload_to='projects/', 
        blank=True, 
        null=True, 
        verbose_name="Image principale"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-start_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('website:project_detail', args=[str(self.slug)])


class ProjectImage(models.Model):
    """Modèle pour la galerie de photos d'un projet"""
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Projet"
    )
    image = models.ImageField(
        upload_to='projects/gallery/', 
        verbose_name="Image"
    )
    caption = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Légende"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Image de projet"
        verbose_name_plural = "Images de projet"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image pour {self.project.title}"


class UserProfile(models.Model):
    """Modèle pour les informations supplémentaires de l'utilisateur"""
    
    # Liste des pays (vous pouvez l'étendre)
    COUNTRY_CHOICES = [
        ('TG', 'Togo'),
        ('BJ', 'Bénin'),
        ('BF', 'Burkina Faso'),
        ('CI', "Côte d'Ivoire"),
        ('ML', 'Mali'),
        ('NE', 'Niger'),
        ('SN', 'Sénégal'),
        ('GN', 'Guinée'),
        ('MR', 'Mauritanie'),
        ('CM', 'Cameroun'),
        ('GA', 'Gabon'),
        ('CD', 'RD Congo'),
        ('CG', 'Congo'),
        ('FR', 'France'),
        ('BE', 'Belgique'),
        ('CH', 'Suisse'),
        ('CA', 'Canada'),
        ('US', 'États-Unis'),
        ('OTHER', 'Autre'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Utilisateur"
    )
    country = models.CharField(
        max_length=5,
        choices=COUNTRY_CHOICES,
        verbose_name="Pays",
        help_text="Pays de résidence"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone sans indicatif (ex: 90XXXXXX)"
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="Prénoms",
        help_text="Prénoms de l'utilisateur"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom de famille de l'utilisateur"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def get_full_name(self):
        """Retourne le nom complet (prénoms + nom)"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_phone_with_country_code(self):
        """Retourne le numéro de téléphone avec l'indicatif du pays"""
        country_codes = {
            'TG': '+228',
            'BJ': '+229',
            'BF': '+226',
            'CI': '+225',
            'ML': '+223',
            'NE': '+227',
            'SN': '+221',
            'GN': '+224',
            'MR': '+222',
            'CM': '+237',
            'GA': '+241',
            'CD': '+243',
            'CG': '+242',
            'FR': '+33',
            'BE': '+32',
            'CH': '+41',
            'CA': '+1',
            'US': '+1',
        }
        code = country_codes.get(self.country, '')
        return f"{code} {self.phone}" if code else self.phone


# Signal pour créer automatiquement un profil lors de la création d'un utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil utilisateur lors de la création d'un utilisateur"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil utilisateur lors de la sauvegarde de l'utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class ContactInfo(models.Model):
    """Modèle pour les informations de contact programmables"""
    
    address = models.CharField(
        max_length=200,
        default="Lomé, Togo",
        verbose_name="Adresse",
        help_text="Adresse complète de l'entreprise"
    )
    address_details = models.CharField(
        max_length=200,
        blank=True,
        default="Quartier administratif",
        verbose_name="Détails de l'adresse",
        help_text="Complément d'adresse (quartier, etc.)"
    )
    email = models.EmailField(
        default="contact@ibcbtp.tg",
        verbose_name="Email de contact"
    )
    phone = models.CharField(
        max_length=20,
        default="+228 XX XX XX XX",
        verbose_name="Téléphone",
        help_text="Format: +228 XX XX XX XX"
    )
    hours = models.CharField(
        max_length=200,
        default="Lundi – Vendredi : 8h00 – 18h00",
        verbose_name="Horaires d'ouverture"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Désactiver pour masquer ces informations"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact Info - {self.email}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule information de contact active
        if self.active:
            ContactInfo.objects.filter(active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_info(cls):
        """Retourne les informations de contact actives"""
        try:
            return cls.objects.get(active=True)
        except cls.DoesNotExist:
            # Retourner un objet par défaut si aucun n'existe
            return cls(
                address="Lomé, Togo",
                address_details="Quartier administratif",
                email="contact@ibcbtp.tg",
                phone="+228 XX XX XX XX",
                hours="Lundi – Vendredi : 8h00 – 18h00"
            )


class Visitor(models.Model):
    """Modèle pour tracker les visiteurs du site"""
    
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    path = models.CharField(max_length=500, blank=True, verbose_name="Chemin visité")
    referer = models.CharField(max_length=500, blank=True, null=True, verbose_name="Référent")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de visite")
    
    class Meta:
        verbose_name = "Visiteur"
        verbose_name_plural = "Visiteurs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"Visiteur {self.ip_address} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
    
    @classmethod
    def get_visitors_count(cls):
        """Retourne le nombre total de visiteurs"""
        return cls.objects.count()
    
    @classmethod
    def get_visitors_today(cls):
        """Retourne le nombre de visiteurs aujourd'hui"""
        from django.utils import timezone
        today = timezone.now().date()
        return cls.objects.filter(created_at__date=today).count()
    
    @classmethod
    def get_visitors_this_week(cls):
        """Retourne le nombre de visiteurs cette semaine"""
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        return cls.objects.filter(created_at__gte=week_ago).count()
    
    @classmethod
    def get_visitors_this_month(cls):
        """Retourne le nombre de visiteurs ce mois"""
        from django.utils import timezone
        from datetime import timedelta
        month_ago = timezone.now() - timedelta(days=30)
        return cls.objects.filter(created_at__gte=month_ago).count()
    
    @classmethod
    def get_visitors_by_day(cls, days=30):
        """Retourne les statistiques de visiteurs par jour pour les N derniers jours"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        
        start_date = timezone.now() - timedelta(days=days)
        visitors = cls.objects.filter(created_at__gte=start_date).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return list(visitors)
