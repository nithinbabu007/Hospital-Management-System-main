from django.urls import path
from . import views

urlpatterns = [

    path('', views.user_profile, name='user_profile'),
    path('appointment_page/', views.appointment_page, name='appointment_page'),
    path('doctors_page/', views.doctors_page, name='doctors_page'),
    path('get-doctors/', views.get_doctors, name="get_doctors"),
    path('booking_appointment/', views.booking_appointment, name="booking_appointment"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('ai_chatbot/', views.ai_chatbot, name="ai_chatbot"),
    path('about_page/', views.about_page, name="about_page"),
    path('service_page/', views.service_page, name="service_page"),
    path('contact_page/', views.contact_page, name="contact_page"),
    path('contact/', views.contact_view, name='contact'),




]