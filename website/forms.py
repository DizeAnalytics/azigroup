from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import Contact


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
                'placeholder': '+223 XX XX XX XX'
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
        if phone:
            # Validation basique du numéro de téléphone
            phone = phone.replace(' ', '').replace('-', '').replace('+', '')
            if not phone.isdigit() or len(phone) < 8:
                raise forms.ValidationError("Veuillez entrer un numéro de téléphone valide.")
        return phone
