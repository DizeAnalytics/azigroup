from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('companies/', views.companies, name='companies'),
    path('companies/<slug:slug>/', views.company_detail, name='company_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('search/', views.search, name='search'),
    
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard administrateur
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    
    # API endpoints
    path('api/contact/', views.contact_ajax, name='contact_ajax'),
    path('api/companies/', views.api_companies, name='api_companies'),
    path('api/news/', views.api_news, name='api_news'),
    
    # SEO
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
