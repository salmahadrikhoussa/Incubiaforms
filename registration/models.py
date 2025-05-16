from django.db import models

class RegistrationStep1(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    terms_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class RegistrationStep2(models.Model):
    project_name = models.CharField(max_length=255)
    project_level = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name

class RegistrationStep3(models.Model):
    CHOICES = (
        ('mentoring', 'Mentorat'),
        ('training', 'Formation'),
        ('financing', 'Financement'),
        ('resources', 'Ressources'),
    )
    choice = models.CharField(max_length=20, choices=CHOICES, blank=True, null=True)

    def __str__(self):
        return "Expectations"

class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    terms_accepted = models.BooleanField(default=False)
    project_name = models.CharField(max_length=255)
    project_level = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=255)
    choice = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name
