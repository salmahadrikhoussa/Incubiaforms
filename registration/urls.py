from django.urls import path
from . import views

urlpatterns = [
    path('step1/', views.registration_step1, name='registration_step1'),
    path('step2/', views.registration_step2, name='registration_step2'),
    path('step3/', views.registration_step3, name='registration_step3'),
    path('thankyou/', views.registration_thankyou, name='registration_thankyou'),
    path('test-email/', views.test_email, name='test_email'),

]