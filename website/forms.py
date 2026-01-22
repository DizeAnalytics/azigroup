from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Contact, UserProfile


class ContactForm(forms.ModelForm):
    """Formulaire de contact"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'company', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+228 XX XX XX XX',
                'pattern': r'\+[0-9\s\-\(\)]+'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre entreprise ou organisation'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Votre message...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('company', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Field('service', css_class='form-group'),
            Field('message', css_class='form-group'),
            Submit('submit', 'Envoyer le message', css_class='btn btn-primary btn-lg')
        )
        
        # Ajouter des classes CSS aux champs
        for field_name, field in self.fields.items():
            field.required = field_name in ['name', 'email', 'message']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Contact.objects.filter(email=email).exists():
            # Optionnel : vérifier si l'email existe déjà
            pass
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Le téléphone est optionnel, donc si vide, on retourne None
        if not phone or not phone.strip():
            return None
        
        # Validation pour accepter l'indicatif du pays + le numéro
        # Format attendu: +228 XX XX XX XX ou +228XXXXXXXX
        phone_cleaned = phone.strip()
        
        # Vérifier que le numéro commence par + (indicatif international)
        if not phone_cleaned.startswith('+'):
            raise forms.ValidationError(
                "Veuillez entrer un numéro de téléphone avec l'indicatif du pays (ex: +228 XX XX XX XX)."
            )
        
        # Extraire uniquement les chiffres après le +
        digits = phone_cleaned[1:].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Vérifier que ce sont bien des chiffres
        if not digits.isdigit():
            raise forms.ValidationError(
                "Le numéro de téléphone ne doit contenir que des chiffres après l'indicatif du pays."
            )
        
        # Vérifier la longueur minimale (indicatif + numéro, au moins 8 chiffres)
        if len(digits) < 8:
            raise forms.ValidationError(
                "Le numéro de téléphone est trop court. Format attendu: +228 XX XX XX XX"
            )
        
        # Vérifier la longueur maximale (indicatif + numéro, max 15 chiffres selon ITU-T)
        if len(digits) > 15:
            raise forms.ValidationError(
                "Le numéro de téléphone est trop long. Format attendu: +228 XX XX XX XX"
            )
        
        # Retourner le numéro formaté avec le +
        return '+' + digits


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription utilisateur"""
    
    email = forms.EmailField(
        required=True,
        label="E-mail *",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre.email@exemple.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        max_length=100,
        label="Prénoms *",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vos prénoms'
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=100,
        label="Nom *",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom de famille'
        })
    )
    country = forms.ChoiceField(
        required=True,
        choices=UserProfile.COUNTRY_CHOICES,
        label="Pays *",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        required=True,
        max_length=20,
        label="Téléphone *",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '90XXXXXX',
            'pattern': '[0-9]{8,15}'
        }),
        help_text="Entrez un numéro de téléphone valide sans l'indicatif de votre pays (ex: 90XXXXXX)"
    )
    password1 = forms.CharField(
        required=True,
        label="Mot de passe *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        }),
        help_text="Au moins 8 caractères"
    )
    password2 = forms.CharField(
        required=True,
        label="Confirmation du mot de passe *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'country', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retirer le champ username du formulaire
        if 'username' in self.fields:
            del self.fields['username']
        
        # Configurer crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'registration-form'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('country', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Field('phone', css_class='form-group'),
            Field('password1', css_class='form-group'),
            Field('password2', css_class='form-group'),
            Submit('submit', "S'inscrire", css_class='btn btn-primary btn-lg w-100')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Nettoyer le numéro (enlever espaces, tirets, etc.)
            phone_cleaned = phone.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            # Vérifier que ce sont bien des chiffres
            if not phone_cleaned.isdigit():
                raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
            
            # Vérifier la longueur (au moins 8 chiffres)
            if len(phone_cleaned) < 8:
                raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
            
            # Vérifier la longueur maximale
            if len(phone_cleaned) > 15:
                raise forms.ValidationError("Le numéro de téléphone est trop long.")
            
            return phone_cleaned
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Utiliser l'email comme username
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Créer ou mettre à jour le profil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = self.cleaned_data['country']
            profile.phone = self.cleaned_data['phone']
            profile.first_name = self.cleaned_data['first_name']
            profile.last_name = self.cleaned_data['last_name']
            profile.save()
        
        return user


class UserLoginForm(AuthenticationForm):
    """Formulaire de connexion utilisateur - accepte email ou username"""
    
    username = forms.CharField(
        required=True,
        label="E-mail ou nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre.email@exemple.com ou nom d\'utilisateur',
            'autofocus': True
        })
    )
    password = forms.CharField(
        required=True,
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne pas utiliser crispy forms ici pour éviter les problèmes CSRF
        # Les widgets sont déjà configurés avec les bonnes classes CSS
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Le backend personnalisé gère la vérification, donc on accepte email ou username
        return username
