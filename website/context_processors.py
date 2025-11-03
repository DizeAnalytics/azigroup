from .models import NavigationLogo, HomePageHero, Company

def navigation_logo(request):
    """Contexte global pour le logo de navigation et les entreprises"""
    active_logo = NavigationLogo.get_active_logo()
    active_hero = HomePageHero.get_active_hero()

    navbar_logo_url = None
    if active_hero and getattr(active_hero, 'background_image', None):
        try:
            navbar_logo_url = active_hero.background_image.url
        except Exception:
            navbar_logo_url = None

    if not navbar_logo_url and active_logo and getattr(active_logo, 'logo', None):
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
    }
