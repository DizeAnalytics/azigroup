"""
Script pour créer un superadmin pour IBC SARL
Ce script crée un superutilisateur avec email comme username et un profil utilisateur complet
"""
import os
import django

# Configuration Django - DOIT être fait AVANT d'importer les modèles
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IBC_SARL.settings')
django.setup()

# Maintenant on peut importer les modèles
from django.contrib.auth import get_user_model
from django.db.models import Q
from website.models import UserProfile

User = get_user_model()

# Informations du superadmin
EMAIL = 'admin@ibcsarl.com'  # Email utilisé comme username
PASSWORD = 'admin123'  # Mot de passe (changez-le en production !)
FIRST_NAME = 'Admin'
LAST_NAME = 'IBC SARL'
COUNTRY = 'TG'  # Togo
PHONE = '90123456'  # Numéro sans indicatif

def create_superadmin():
    """Crée un superadmin avec profil utilisateur complet"""
    try:
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(email=EMAIL).exists() or User.objects.filter(username=EMAIL).exists():
            user = User.objects.filter(Q(username=EMAIL) | Q(email=EMAIL)).first()
            if user:
                # Mettre à jour le mot de passe et les permissions
                user.set_password(PASSWORD)
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.first_name = FIRST_NAME
                user.last_name = LAST_NAME
                user.save()
                
                # Mettre à jour ou créer le profil
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.first_name = FIRST_NAME
                profile.last_name = LAST_NAME
                profile.country = COUNTRY
                profile.phone = PHONE
                profile.save()
                
                print(f"[OK] Superadmin '{EMAIL}' mis a jour avec succes !")
                print(f"   - Mot de passe reinitialise")
                print(f"   - Permissions administrateur activees")
                print(f"   - Profil utilisateur mis a jour")
                return user
        else:
            # Créer un nouvel utilisateur
            user = User.objects.create_superuser(
                username=EMAIL,  # Email comme username
                email=EMAIL,
                password=PASSWORD,
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            # Créer le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.first_name = FIRST_NAME
            profile.last_name = LAST_NAME
            profile.country = COUNTRY
            profile.phone = PHONE
            profile.save()
            
            print(f"[OK] Superadmin '{EMAIL}' cree avec succes !")
            print(f"   - Email/Username: {EMAIL}")
            print(f"   - Mot de passe: {PASSWORD}")
            print(f"   - Nom complet: {FIRST_NAME} {LAST_NAME}")
            print(f"   - Pays: {COUNTRY}")
            print(f"   - Telephone: {PHONE}")
            print(f"\n[INFO] Vous pouvez maintenant vous connecter a:")
            print(f"   http://127.0.0.1:8000/login/")
            print(f"\n[ATTENTION] IMPORTANT: Changez le mot de passe en production !")
            return user
            
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la creation du superadmin: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    create_superadmin()
