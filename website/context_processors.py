from .models import NavigationLogo, HomePageHero, Company

def navigation_logo(request):
    """Contexte global pour le logo de navigation et les entreprises"""
    active_logo = NavigationLogo.get_active_logo()
    active_hero = HomePageHero.get_active_hero()

    navbar_logo_url = None
    # Priorité au logo de navigation (pas au background_image du hero)
    if active_logo and getattr(active_logo, 'logo', None):
        try:
            navbar_logo_url = active_logo.logo.url
        except Exception:
            navbar_logo_url = None

    # Récupérer les entreprises actives pour le footer
    companies = Company.objects.filter(active=True).order_by('name')

    return {
        'navigation_logo': active_logo,
        'navbar_logo_url': navbar_logo_url,
        'companies': companies,
        'hero_section': active_hero,  # Ajouter le hero pour utilisation dans les templates
    }
