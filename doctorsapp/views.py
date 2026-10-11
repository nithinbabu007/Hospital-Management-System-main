from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import authenticate,login
from django.contrib import messages

from django.contrib.auth.models import User
from adminapp.models import *
from doctorsapp.models import *
from django.core.mail import send_mail
from django.conf import settings
import random
from adminapp.views import *



def sigin_page(request):

    return render(request,'sigin_page.html')

#dcoctor section
def  doctor_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=username+"123"
        password=request.POST.get('password')
        doctor = doctordb.objects.filter(doc_name__contains=username).first()
        if doctor:
            otp = random.randint(100000,999999)

            request.session['username'] = username
            request.session['password'] = password
            request.session['otp'] = otp

            if pass1 == password:
                send_mail(
                'Admin Login Alert',
                f'Admin {username} has logged into the Hospital Management System.Admin Login OTP ,\n\n  ---Your OTP for admin login is {otp}',
                settings.EMAIL_HOST_USER,
                [doctor.doc_email] if doctor.doc_email else [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
                return redirect(verify_otp)
            else:
                messages.error(request, "Invalid Password ❌")
        else:
            messages.error(request, "Doctor not found ❌")
            return render(request, 'sigin_page.html')

    return render(request,'sigin_page.html')

 #otp page
def verify_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(user_otp) == str(session_otp):

           
            

           
            messages.success(request, "OTP Verified Successfully ✅")

            return redirect(doctor_page)

        else:
            messages.error(request, "Invalid OTP ❌")

            return render(request,'otp_page.html',{'error':'Invalid OTP'})

    return render(request,'otp_page.html')

# Doctor Page View
def doctor_page(request):
    username = request.session.get('username')
    doctor = doctordb.objects.filter(doc_name=username).first()
    
    total_appointments = appointmentdb.objects.count()


    return render(request, "doctor_page.html", {"username": username, "doctor": doctor
                                                , "total_appointments": total_appointments})

#doctor page logout
def doctor_logout(request):
    username = request.session.get('username')

    if not username:
       return redirect(sigin_page)
    del request.session['username']
    del request.session['password']
    
    return redirect(sigin_page)


def attendance_page(request):
    doctor = doctordb.objects.get(doc_name=request.session['username'])

    today = timezone.now().date()

    # check today attendance
    already_marked = Attendance.objects.filter(
        doctor=doctor,
        date=today
    ).exists()

    
    present = Attendance.objects.filter(
        doctor=doctor,
        date__month=today.month,
        date__year=today.year,
        status='Present'
    ).count()

    absent = 30 - present   # simple logic

    return render(request, 'attendance_page.html', {
        'doctor': doctor,
        'present': present,
        'absent': absent,
        'already_marked': already_marked
    })

#qr email

import uuid
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from django.utils import timezone
from django.shortcuts import redirect
from .models import Attendance, doctordb
from django.urls import reverse



def mark_attendance(request):
    if request.method == "POST":
        doctor = doctordb.objects.get(doc_name=request.session['username'])
        today = timezone.now().date()
        date_str = today.strftime("%d-%m-%Y")   # 25-03-2026
        day_str = today.strftime("%A")  
        print("Checking existing attendance...")
        # prevent duplicate
        if Attendance.objects.filter(doctor=doctor, date=today).exists():
             return redirect('attendance_page')

        # create attendance
        attendance = Attendance.objects.create(
            doctor=doctor,
            date=today,
            status='Pending',
            qr_token=uuid.uuid4()
        )

        # create QR URL
        qr_url = request.build_absolute_uri(
            reverse('verify_attendance', args=[attendance.qr_token])
        )
        print("QR URL:", qr_url)
        # generate QR image
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        print("Doctor email:", doctor.doc_email)
        # send em  ail
        email = EmailMessage(
            subject="Your Attendance QR Code",
            body=f"""
Hello Doctor,

Please scan the QR code to mark your attendance.

📅 Date: {date_str}
📆 Day: {day_str}

Thank you.
""",
            to=[doctor.doc_email],

        )

        email.attach('qr.png', buffer.getvalue(), 'image/png')
        email.send(  fail_silently=False)

        return redirect('attendance_page')
   

#QR Verification View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

def verify_attendance(request, token):
    attendance = get_object_or_404(Attendance, qr_token=token)

    if attendance.status == 'Present':
        return redirect('view_attendance')   # ✅ redirect instead of JSON

    from django.utils import timezone
    if attendance.date != timezone.now().date():
        return JsonResponse({'message': 'QR expired ❌'})

    attendance.status = 'Present'
    attendance.save()

    return redirect('view_attendance')   # or show error page


#docotr appooinmets
from userapp.models import *
from django.utils import timezone

def doctor_appointments(request):
    doctor_name = request.session.get('username')
    doctor = doctordb.objects.filter(doc_name=doctor_name).first()


    appointments = appointmentdb.objects.filter(
        doctor=doctor_name
    ).order_by('-date')

    total_appointments = appointments.count()

    today = timezone.now().date()
    today_appointments = appointmentdb.objects.filter(
        doctor=doctor_name,
        date=today
    )

    return render(request, 'appoinments_doc.html', {
        'appointments': appointments,
        'today_appointments': today_appointments,
        'total_appointments': total_appointments,
        'doctor': doctor

    })

#cancel/confirm appointment status (doctor's own appointments only)

def doctor_cancel_appointment(request, appt_id):
    doctor_name = request.session.get('username')
    appt = get_object_or_404(appointmentdb, id=appt_id, doctor=doctor_name)
    appt.status = 'Cancelled'
    appt.save()
    messages.success(request, "Appointment Cancelled ✅")
    return redirect(doctor_appointments)

def doctor_confirm_appointment(request, appt_id):
    doctor_name = request.session.get('username')
    appt = get_object_or_404(appointmentdb, id=appt_id, doctor=doctor_name)
    appt.status = 'Confirmed'
    appt.save()
    messages.success(request, "Appointment Confirmed ✅")
    return redirect(doctor_appointments)
