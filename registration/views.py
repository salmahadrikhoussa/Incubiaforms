from django.shortcuts import render, redirect
from .forms import RegistrationStep1Form, RegistrationStep2Form, RegistrationStep3Form
from django.http import HttpResponse
from .models import User, RegistrationStep1, RegistrationStep2
from django.core.mail import send_mail
from django.conf import settings

def registration_step1(request):
    if request.method == 'POST':
        form = RegistrationStep1Form(request.POST)
        if form.is_valid():
            step1 = form.save()
            request.session['step1_id'] = step1.id
            return redirect('registration_step2')
    else:
        form = RegistrationStep1Form()
    return render(request, 'registration/step1.html', {'form': form})

def registration_step2(request):
    if request.method == 'POST':
        form = RegistrationStep2Form(request.POST)
        if form.is_valid():
            step2 = form.save()
            request.session['step2_id'] = step2.id
            return redirect('registration_step3')
    else:
        form = RegistrationStep2Form()
    return render(request, 'registration/step2.html', {'form': form})

def registration_step3(request):
    if request.method == 'POST':
        form = RegistrationStep3Form(request.POST)
        if form.is_valid():
            step3 = form.save()
            
            # Récupérer les données des étapes précédentes
            step1 = RegistrationStep1.objects.get(id=request.session['step1_id'])
            step2 = RegistrationStep2.objects.get(id=request.session['step2_id'])
            
            # Créer l'utilisateur
            user = User.objects.create(
                full_name=step1.full_name,
                email=step1.email,
                password=step1.password,
                phone_number=step1.phone_number,
                city=step1.city,
                terms_accepted=step1.terms_accepted,
                project_name=step2.project_name,
                project_level=step2.project_level,
                description=step2.description,
                industry=step2.industry,
                choice=step3.choice,
            )
            
            # Envoyer l'email de notification à l'administrateur
            sujet = f"Nouvelle candidature: {user.full_name}"
            message = f"""
            Une nouvelle candidature a été soumise:
            
            Informations personnelles:
            - Nom complet: {user.full_name}
            - Email: {user.email}
            - Téléphone: {user.phone_number}
            - Ville: {user.city}
            
            Détails du projet:
            - Nom du projet: {user.project_name}
            - Niveau du projet: {user.project_level}
            - Description: {user.description}
            - Industrie: {user.industry}
            - Choix d'accompagnement: {user.choice}
            """
            
            send_mail(
                sujet,
                message,
                settings.EMAIL_HOST_USER,  # De
                [settings.ADMIN_EMAIL],    # À
                fail_silently=False,
            )
            
            return redirect('registration_thankyou')
    else:
        form = RegistrationStep3Form()
    return render(request, 'registration/step3.html', {'form': form})

def registration_thankyou(request):
    return render(request, 'registration/thankyou.html')
# Dans un fichier views.py (peut être dans une application de test)
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def test_email(request):
    sujet = "Test d'envoi d'email depuis Django"
    message = "Si vous recevez ce message, la configuration de l'email fonctionne correctement!"
    
    send_mail(
        sujet,
        message,
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    
    return HttpResponse("Email de test envoyé!")

