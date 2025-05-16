from django import forms
from .models import RegistrationStep1, RegistrationStep2, RegistrationStep3
from django.core.exceptions import ValidationError
import re

class RegistrationStep1Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Numéro de téléphone')  # Utiliser CharField

    class Meta:
        model = RegistrationStep1
        fields = ['full_name', 'email', 'password', 'phone_number', 'city', 'terms_accepted']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        if len(phone_number) != 10:
            raise forms.ValidationError("Le numéro de téléphone doit contenir 10 chiffres.")
        return phone_number

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        return password

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if RegistrationStep1.objects.filter(full_name=full_name).exists():
            raise ValidationError("Ce nom est déjà utilisé.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Adresse e-mail invalide.")
        if RegistrationStep1.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wilayas = [
            ("Adrar", "Adrar"), ("Chlef", "Chlef"), ("Laghouat", "Laghouat"), ("Oum El Bouaghi", "Oum El Bouaghi"),
            ("Batna", "Batna"), ("Béjaïa", "Béjaïa"), ("Biskra", "Biskra"), ("Béchar", "Béchar"), ("Blida", "Blida"),
            ("Bouira", "Bouira"), ("Tamanrasset", "Tamanrasset"), ("Tébessa", "Tébessa"), ("Tlemcen", "Tlemcen"),
            ("Tiaret", "Tiaret"), ("Tizi Ouzou", "Tizi Ouzou"), ("Alger", "Alger"), ("Djelfa", "Djelfa"), ("Jijel", "Jijel"),
            ("Sétif", "Sétif"), ("Saïda", "Saïda"), ("Skikda", "Skikda"), ("Sidi Bel Abbès", "Sidi Bel Abbès"),
            ("Annaba", "Annaba"), ("Guelma", "Guelma"), ("Constantine", "Constantine"), ("Médéa", "Médéa"),
            ("Mostaganem", "Mostaganem"), ("M'Sila", "M'Sila"), ("Mascara", "Mascara"), ("Ouargla", "Ouargla"),
            ("Oran", "Oran"), ("El Bayadh", "El Bayadh"), ("Illizi", "Illizi"), ("Bordj Bou Arreridj", "Bordj Bou Arreridj"),
            ("Boumerdès", "Boumerdès"), ("El Tarf", "El Tarf"), ("Tindouf", "Tindouf"), ("Tissemsilt", "Tissemsilt"),
            ("El Oued", "El Oued"), ("Khenchela", "Khenchela"), ("Souk Ahras", "Souk Ahras"), ("Tipaza", "Tipaza"),
            ("Mila", "Mila"), ("Aïn Defla", "Aïn Defla"), ("Naâma", "Naâma"), ("Aïn Témouchent", "Aïn Témouchent"),
            ("Ghardaïa", "Ghardaïa"), ("Relizane", "Relizane")
        ]
        self.fields['city'].widget = forms.Select(choices=wilayas)
        self.fields['terms_accepted'].required = True



class RegistrationStep2Form(forms.ModelForm):
    class Meta:
        model = RegistrationStep2
        fields = ['project_name', 'project_level', 'description', 'industry']

    project_level = forms.ChoiceField(choices=[
        ('Lancement', 'Lancement'),
        ('En cours de développement', 'En cours de développement'),
        ('En cours de création', 'En cours de création'),
        ('Projet en croissance', 'Projet en croissance'),
    ])

    industry = forms.ChoiceField(choices=[
        ('Tech', 'Tech'),
        ('Industries', 'Industries'),
        ('Technologie & Logiciels', 'Technologie & Logiciels'),
        ('Santé & Bien-être', 'Santé & Bien-être'),
        ('Éducation & Formation', 'Éducation & Formation'),
    ])
    def clean_description(self):
        description = self.cleaned_data['description']
        words = description.split()
        if len(words) > 50:
            raise ValidationError("La description ne doit pas dépasser 50 mots.")
        return description

class RegistrationStep3Form(forms.ModelForm):
    class Meta:
        model = RegistrationStep3
        fields = ['choice']

    choice = forms.ChoiceField(
        choices=RegistrationStep3.CHOICES,
        widget=forms.RadioSelect,
        required=True,
        error_messages={'required': "Vous devez choisir une option."},
    )