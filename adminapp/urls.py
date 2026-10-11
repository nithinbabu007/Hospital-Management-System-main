from django.urls import path
from adminapp import views
urlpatterns = [
    
    path("admin_page/",views.admin_page,name="admin_page"),
    path("prime/",views.admin_loginpage,name="admin_loginpage"),
    path("admin_login",views.admin_login,name="admin_login"),
    path("admin_logout",views.admin_logout,name="admin_logout"),
    path("view_doctors",views.view_doctors,name="view_doctors"),
    path("view_departments",views.view_departments,name="view_departments"),
    path("save_department",views.save_department,name="save_department"),
    path("save_doctors",views.save_doctors,name="save_doctors"),
    path('doctor_list', views.doctor_list, name='doctor_list'),
    path('verify_otp/',views.verify_otp,name='otp_page'),
    path('delete_doctor/<int:doc_id>/',views.delete_doctor,name='delete_doctor'),
    path('edit_doctor_page/<int:doc_id>/',views.edit_doctor_page,name='edit_doctor_page'),
    path('update_doctor/<int:doc_id>/',views.update_doctor,name='update_doctor'),
    path('scan_page/', views.scan_page, name='scan_page'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('view_department/', views.view_department, name='view_department'),
    path('delete_department/<int:idd>/', views.delete_department, name='delete_department'),
    path('update_department/<int:idd>/', views.update_department, name='update_department'),
    path('appoinment_list', views.appoinment_list, name='appoinment_list'),
    path('cancel_appointment/<int:appt_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('confirm_appointment/<int:appt_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('message_list', views.message_list, name='message_list'),


]