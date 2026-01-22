"""
Backend d'authentification personnalisé pour permettre la connexion avec email
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailBackend(ModelBackend):
    """
    Backend d'authentification qui permet de se connecter avec email ou username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authentifie un utilisateur avec email ou username
        """
        if username is None:
            username = kwargs.get('email')
        
        if username is None or password is None:
            return None
        
        try:
            # Essayer de trouver l'utilisateur par email ou username
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # Retourner None si l'utilisateur n'existe pas
            return None
        except User.MultipleObjectsReturned:
            # Si plusieurs utilisateurs ont le même email, prendre le premier
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        
        # Vérifier le mot de passe
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
