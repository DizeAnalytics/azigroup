from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Contact, Company, News, Setting, Testimonial, HomePageHero, NavigationLogo
from .forms import ContactForm
import json


def index(request):
    """Page d'accueil"""
    companies = Company.objects.filter(active=True)
    recent_news = News.objects.filter(published=True).order_by('-created_at')[:3]
    testimonials = Testimonial.objects.filter(active=True).order_by('-created_at')[:3]
    hero_section = HomePageHero.get_active_hero()
    
    context = {
        'companies': companies,
        'news': recent_news,
        'testimonials': testimonials,
        'hero_section': hero_section,
    }
    return render(request, 'website/index.html', context)


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


def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(
                request, 
                'Votre message a été envoyé avec succès ! Nous vous contacterons bientôt.'
            )
            return redirect('website:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'website/contact.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """API AJAX pour le formulaire de contact"""
    try:
        data = json.loads(request.body)
        form = ContactForm(data)
        
        if form.is_valid():
            contact = form.save()
            return JsonResponse({
                'success': True, 
                'message': 'Message envoyé avec succès'
            })
        else:
            return JsonResponse({
                'success': False, 
                'errors': form.errors,
                'message': 'Veuillez corriger les erreurs'
            })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'message': 'Données JSON invalides'
        })


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
        
        results = {
            'news': news_results,
            'companies': company_results,
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
    
    context = {
        'companies': companies,
        'news': news,
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