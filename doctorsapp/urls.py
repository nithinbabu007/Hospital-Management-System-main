from django.urls import path
from doctorsapp import views

urlpatterns = [
    
    path('sigin_page/',views.sigin_page,name="sigin_page"),
    path('doctor_login/',views.doctor_login,name="doctor_login"),
    path('doctor_page/',views.doctor_page,name="doctor_page"),
    path('doctor_logout/',views.doctor_logout,name="doctor_logout"),
    path('verify_otp/',views.verify_otp,name='otp_page'),
    path('attendance_page/',views.attendance_page,name='attendance_page'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('verify-attendance/<uuid:token>/', views.verify_attendance, name='verify_attendance'),   
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('cancel_appointment/<int:appt_id>/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),
    path('confirm_appointment/<int:appt_id>/', views.doctor_confirm_appointment, name='doctor_confirm_appointment'),


   
]