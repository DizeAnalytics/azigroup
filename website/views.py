from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Contact, Company, News, Setting, Testimonial, HomePageHero, HomePageSlide, NavigationLogo, Project, ContactInfo, Visitor, AboutSectionImage
from .forms import ContactForm, UserRegistrationForm, UserLoginForm
import json


def index(request):
    """Page d'accueil"""
    # Enregistrer la visite
    try:
        Visitor.objects.create(
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path,
            referer=request.META.get('HTTP_REFERER', '')
        )
    except Exception:
        pass  # Ignorer les erreurs de tracking
    
    companies = Company.objects.filter(active=True)
    recent_news = News.objects.filter(published=True).order_by('-created_at')[:3]
    testimonials = Testimonial.objects.filter(active=True).order_by('-created_at')[:3]
    hero_section = HomePageHero.get_active_hero()
    homepage_slides = HomePageSlide.objects.filter(active=True).order_by('order', '-created_at')
    about_image = AboutSectionImage.get_active_image()
    
    context = {
        'companies': companies,
        'news': recent_news,
        'testimonials': testimonials,
        'hero_section': hero_section,
        'homepage_slides': homepage_slides,
        'about_image': about_image,
    }
    return render(request, 'website/index.html', context)


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def about(request):
    """Page À propos"""
    companies = Company.objects.filter(active=True)
    
    context = {
        'companies': companies,
    }
    return render(request, 'website/about.html', context)


def companies(request):
    """Page des entreprises"""
    companies = Company.objects.filter(active=True)
    hero_section = HomePageHero.get_active_hero()
    
    context = {
        'companies': companies,
        'hero_section': hero_section,
    }
    return render(request, 'website/companies.html', context)


def company_detail(request, slug):
    """Détail d'une entreprise"""
    company = get_object_or_404(Company, slug=slug, active=True)
    
    context = {
        'company': company,
    }
    return render(request, 'website/company_detail.html', context)


def project_list(request):
    """Liste des projets"""
    status = request.GET.get('status')
    company_slug = request.GET.get('company')
    
    projects = Project.objects.all()
    
    if status:
        projects = projects.filter(status=status)
    
    if company_slug:
        projects = projects.filter(company__slug=company_slug)
        
    projects = projects.order_by('-start_date')
    
    # Pagination
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    companies = Company.objects.filter(active=True)
    
    context = {
        'projects': projects_page,
        'companies': companies,
        'current_status': status,
        'current_company': company_slug,
    }
    return render(request, 'website/project_list.html', context)


def project_detail(request, slug):
    """Détail d'un projet"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(partners__in=project.partners.all()).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'website/project_detail.html', context)


def news_list(request):
    """Liste des actualités"""
    news_list = News.objects.filter(published=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(news_list, 6)  # 6 articles par page
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    context = {
        'news': news,
    }
    return render(request, 'website/news_list.html', context)


def news_detail(request, slug):
    """Détail d'une actualité"""
    news = get_object_or_404(News, slug=slug, published=True)
    
    # Articles similaires (même catégorie ou récents)
    related_news = News.objects.filter(
        published=True
    ).exclude(id=news.id).order_by('-created_at')[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'website/news_detail.html', context)


@login_required(login_url='website:login')
def contact(request):
    """Page de contact - nécessite une connexion"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = form.save()
                messages.success(
                    request, 
                    'Votre message a été envoyé avec succès ! Nous vous contacterons bientôt.'
                )
                return redirect('website:contact')
            except Exception as e:
                messages.error(
                    request,
                    f'Une erreur est survenue lors de l\'envoi du message: {str(e)}'
                )
    else:
        # Pré-remplir le formulaire avec les données de l'utilisateur connecté
        initial_data = {}
        if request.user.is_authenticated:
            # Récupérer le profil utilisateur s'il existe
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                initial_data = {
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'phone': profile.get_phone_with_country_code() if profile.phone else '',
                }
            else:
                # Si pas de profil, utiliser les données de base de l'utilisateur
                initial_data = {
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                }
        form = ContactForm(initial=initial_data)
    
    # Récupérer les informations de contact depuis la base de données
    try:
        contact_info = ContactInfo.get_active_info()
    except Exception:
        # Si le modèle n'existe pas encore (migration pas faite), utiliser des valeurs par défaut
        contact_info = ContactInfo(
            address="Lomé, Togo",
            address_details="Quartier administratif",
            email="contact@ibcbtp.tg",
            phone="+228 XX XX XX XX",
            hours="Lundi – Vendredi : 8h00 – 18h00"
        )
    
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'website/contact.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """API AJAX pour le formulaire de contact"""
    import logging
    import traceback
    logger = logging.getLogger(__name__)
    
    try:
        # Log les données reçues pour le débogage
        raw_data = request.body.decode('utf-8')
        logger.info(f"Données reçues: {raw_data}")
        
        data = json.loads(raw_data)
        logger.info(f"Données parsées: {data}")
        
        form = ContactForm(data)
        
        if form.is_valid():
            try:
                contact = form.save()
                logger.info(f"Contact sauvegardé avec succès: {contact.id}")
                return JsonResponse({
                    'success': True, 
                    'message': 'Message envoyé avec succès'
                })
            except Exception as e:
                # Log l'erreur complète pour le débogage
                error_traceback = traceback.format_exc()
                logger.error(f"Erreur lors de la sauvegarde du contact: {str(e)}")
                logger.error(f"Traceback: {error_traceback}")
                print(f"ERREUR SAUVEGARDE: {str(e)}")
                print(f"TRACEBACK: {error_traceback}")
                return JsonResponse({
                    'success': False, 
                    'message': f'Erreur lors de la sauvegarde: {str(e)}'
                }, status=500)
        else:
            # Formater les erreurs pour l'affichage
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            
            logger.warning(f"Formulaire invalide: {form.errors}")
            print(f"ERREURS DE VALIDATION: {form.errors}")
            
            return JsonResponse({
                'success': False, 
                'errors': form.errors,
                'message': 'Veuillez corriger les erreurs: ' + ' | '.join(error_messages)
            }, status=400)
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON: {str(e)}")
        print(f"ERREUR JSON: {str(e)}")
        return JsonResponse({
            'success': False, 
            'message': f'Données JSON invalides: {str(e)}'
        }, status=400)
    except Exception as e:
        # Capturer toutes les autres exceptions
        error_traceback = traceback.format_exc()
        logger.error(f"Erreur inattendue dans contact_ajax: {str(e)}")
        logger.error(f"Traceback: {error_traceback}")
        print(f"ERREUR INATTENDUE: {str(e)}")
        print(f"TRACEBACK: {error_traceback}")
        return JsonResponse({
            'success': False, 
            'message': f'Erreur inattendue: {str(e)}'
        }, status=500)


def search(request):
    """Page de recherche"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Recherche dans les actualités
        news_results = News.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query),
            published=True
        )
        
        # Recherche dans les entreprises
        company_results = Company.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            active=True
        )
        
        # Recherche dans les projets
        project_results = Project.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(client__icontains=query) |
            Q(location__icontains=query)
        )
        
        results = {
            'news': news_results,
            'companies': company_results,
            'projects': project_results,
            'query': query,
        }
    
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'website/search.html', context)


def testimonials(request):
    """Page des témoignages"""
    testimonials = Testimonial.objects.filter(active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(testimonials, 9)  # 9 témoignages par page
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'website/testimonials.html', context)


def sitemap(request):
    """Génération simple du sitemap"""
    companies = Company.objects.filter(active=True)
    news = News.objects.filter(published=True)
    projects = Project.objects.all()
    
    context = {
        'companies': companies,
        'news': news,
        'projects': projects,
    }
    return render(request, 'website/sitemap.xml', context, content_type='application/xml')


def robots_txt(request):
    """Fichier robots.txt"""
    return render(request, 'website/robots.txt', content_type='text/plain')


# Vues pour l'API (optionnel)
def api_companies(request):
    """API pour les entreprises"""
    companies = Company.objects.filter(active=True)
    data = []
    
    for company in companies:
        data.append({
            'id': company.id,
            'name': company.name,
            'slug': company.slug,
            'description': company.description,
            'icon': company.icon,
            'gradient': company.gradient,
            'services': company.get_services_list(),
            'kpis': company.get_kpis_list(),
            'url': company.get_absolute_url(),
        })
    
    return JsonResponse({'companies': data})


def api_news(request):
    """API pour les actualités"""
    news = News.objects.filter(published=True).order_by('-created_at')
    data = []
    
    for article in news:
        data.append({
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'excerpt': article.get_excerpt(),
            'image_url': article.get_image_url(),
            'created_at': article.created_at.isoformat(),
            'url': article.get_absolute_url(),
        })
    
    return JsonResponse({'news': data})


def register(request):
    """Vue pour l'inscription"""
    if request.user.is_authenticated:
        return redirect('website:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connecter automatiquement l'utilisateur après l'inscription
            login(request, user)
            messages.success(
                request,
                f'Bienvenue {user.get_full_name()} ! Votre compte a été créé avec succès.'
            )
            return redirect('website:index')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Inscription'
    }
    return render(request, 'website/register.html', context)


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def user_login(request):
    """Vue pour la connexion"""
    if request.user.is_authenticated:
        # Si l'utilisateur est déjà connecté, rediriger selon son statut
        if request.user.is_staff:
            return redirect('website:dashboard')
        return redirect('website:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            # Le backend personnalisé gère maintenant l'authentification par email
            username = form.cleaned_data.get('username')  # Peut être email ou username
            password = form.cleaned_data.get('password')
            
            # Authentifier avec le backend personnalisé (qui accepte email ou username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name() or user.username} !')
                # Rediriger les administrateurs vers le dashboard
                if user.is_staff:
                    return redirect('website:dashboard')
                # Rediriger vers la page demandée ou la page d'accueil
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('website:index')
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
        else:
            # Afficher les erreurs du formulaire
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
    else:
        # Pour GET, on doit aussi passer request à AuthenticationForm
        form = UserLoginForm(request=request)
    
    context = {
        'form': form,
        'title': 'Connexion'
    }
    return render(request, 'website/login.html', context)


@login_required
def user_logout(request):
    """Vue pour la déconnexion"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('website:index')


def is_admin(user):
    """Vérifie si l'utilisateur est un administrateur"""
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin, login_url='website:login')
def dashboard(request):
    """Tableau de bord administrateur"""
    # Messages de contact récents
    recent_contacts = Contact.objects.all().order_by('-created_at')[:10]
    total_contacts = Contact.objects.count()
    new_contacts = Contact.objects.filter(status='nouveau').count()
    
    # Statistiques des visiteurs
    total_visitors = Visitor.get_visitors_count()
    visitors_today = Visitor.get_visitors_today()
    visitors_this_week = Visitor.get_visitors_this_week()
    visitors_this_month = Visitor.get_visitors_this_month()
    
    # Données pour le graphique des visiteurs (30 derniers jours)
    visitors_by_day = Visitor.get_visitors_by_day(days=30)
    
    # Préparer les données pour le graphique
    chart_labels = []
    chart_data = []
    for item in visitors_by_day:
        chart_labels.append(item['date'].strftime('%d/%m'))
        chart_data.append(item['count'])
    
    # Autres statistiques
    companies_count = Company.objects.filter(active=True).count()
    news_count = News.objects.filter(published=True).count()
    projects_count = Project.objects.count()
    
    context = {
        'recent_contacts': recent_contacts,
        'total_contacts': total_contacts,
        'new_contacts': new_contacts,
        'total_visitors': total_visitors,
        'visitors_today': visitors_today,
        'visitors_this_week': visitors_this_week,
        'visitors_this_month': visitors_this_month,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'companies_count': companies_count,
        'news_count': news_count,
        'projects_count': projects_count,
    }
    return render(request, 'website/dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='website:login')
def contact_detail(request, contact_id):
    """Vue pour afficher le détail d'un message de contact"""
    contact = get_object_or_404(Contact, id=contact_id)
    
    # Marquer le message comme lu s'il est nouveau
    if contact.status == 'nouveau':
        contact.status = 'lu'
        contact.save()
    
    context = {
        'contact': contact,
    }
    return render(request, 'website/contact_detail.html', context)
