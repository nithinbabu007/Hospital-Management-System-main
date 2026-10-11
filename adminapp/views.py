from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import authenticate,login
from django.contrib import messages

from django.contrib.auth.models import User
from adminapp.models import *
from doctorsapp.models import *
from userapp.models import *
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.
def admin_page(request):
    # doctors = Doctor.objects.count()
    # patients = Patient.objects.count()
    # appointments = Appointment.objects.count()
    departments = departmentdb.objects.all()
    doctors = doctordb.objects.all()
    attendances = Attendance.objects.all()
     # count present & absent for today
    present = attendances.filter(status='Present').count()
    total = attendances.count()
    absent = total - present
    appn=appointmentdb.objects.count()
    mss=ContactMessage.objects.count()
    



    return render(request, 'index.html',{'departments':departments,
                                                'doctor':doctors,
                                                'attendances': attendances
                                                ,'present': present,
        'absent': absent,
        'appn':appn,
        'mss':mss,
        })

def admin_loginpage(request):
    return render(request, 'admin_login_page.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        

    if User.objects.filter(username__contains=username).exists(): # check if user exists

        user=authenticate(request, username=username, password=password)# check if password is correct
        if user is not None and  user:# if user exists and password is correct
            otp = random.randint(100000,999999)

            
            
            request.session['username'] = username
            request.session['password'] = password
            request.session['otp'] = otp
            request.session['username'] = username
            send_mail(
                'Admin Login Alert',
                f'Admin {username} has logged into the Hospital Management System.Admin Login OTP ,\n\n  ---Your OTP for admin login is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email] if user.email else [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            return redirect(verify_otp)

            
        else:
            messages.error(request, "Invalid login credentials")
        return redirect(admin_loginpage)

#otp section
from django.contrib.auth import login
from django.contrib.auth.models import User

def verify_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(user_otp) == str(session_otp):

            username = request.session.get('username')
            user = User.objects.get(username=username)

            login(request,user)
            messages.success(request, "OTP Verified Successfully ✅")

            return redirect('admin_page')

        else:
            messages.error(request, "Invalid OTP ❌")

            return render(request,'otp_page.html',{'error':'Invalid OTP'})

    return render(request,'otp_page.html')
        


#admin logout

def admin_logout(request):
    username = request.session.get('username')

    if not username:
       return redirect(admin_loginpage)
    del request.session['username']
    del request.session['password']
    
    return redirect(admin_loginpage)


# doctor page

def view_doctors(request):
    departments = departmentdb.objects.all()
    doctors = doctordb.objects.all()
    appn=appointmentdb.objects.count()

    return render(request,'Doctor_section.html',{'departments':departments,
                                                'doctors':doctors,
                                                'appn':appn})

#show add doctors
def doctor_list(request):
    doctors = doctordb.objects.all()
    appn=appointmentdb.objects.count()

    return render(request, "view_doctor.html", {"doctors": doctors,
                                                'appn':appn})

#svae doctors
def save_doctors(request):
    if request.method == "POST":

        doc_name = request.POST.get('name')
        doc_dept = request.POST.get('department')
        doc_phn = request.POST.get('phone')
        doc_email = request.POST.get('email')
        doc_image = request.FILES.get('image')
        doc_quali = request.POST.get('doc_quali')

        doctordb.objects.create(
            doc_name=doc_name,
            doc_dpt=doc_dept,
            doc_phone=doc_phn,
            doc_email=doc_email,
            doc_image=doc_image,
            doc_quali=doc_quali

        )
    

        messages.success(request, "Doctor Added Successfully ✅")
         # Send email to doctor
        send_mail(
            'Welcome to PrimeCare Medical Institute',
            f'Dear Dr. {doc_name},\n\nYou have been successfully added to the hospital system.\nDepartment: {doc_dept}\n\nThank you.',
            settings.EMAIL_HOST_USER,
            [doc_email],
            fail_silently=False,
        )

        


        return redirect(view_doctors)
    

   
        




#view department

def view_departments(request):
    departments = departmentdb.objects.all()
    appn=appointmentdb.objects.count()
    return render(request,'department_section.html',{'departments':departments,
                                                    'appn':appn})
             

#save deparrtment

def save_department(request):

    if request.method == "POST":

        dpt_name = request.POST.get('dpt_name')
        dpt_des = request.POST.get('dpt_des')
        dpt_phone = request.POST.get('dpt_phone')
        dpt_email = request.POST.get('dpt_email')
        dpt_image = request.FILES.get('dpt_image')

        departmentdb.objects.create(
            dpt_name=dpt_name,
            dpt_des=dpt_des,
            dpt_phone=dpt_phone,
            dpt_email=dpt_email,
            dpt_image=dpt_image
        )

        messages.success(request, "Department Added Successfully ✅")

        


        return redirect(view_departments)


#delete doctor

def delete_doctor(request, doc_id):
    doctor = doctordb.objects.get(id=doc_id)
    doctor.delete()
    messages.success(request, "Doctor Deleted Successfully ✅")
    return redirect(doctor_list)
    

#edit deoctor apge
def edit_doctor_page(request, doc_id):
    doctor = doctordb.objects.get(id=doc_id)
    return render(request, 'edit_doctor.html', {'doctor': doctor})


#edit docotr
def update_doctor(request, doc_id):

    doctor = get_object_or_404(doctordb, id=doc_id)
    if request.method=="POST":
        doc_name = request.POST.get('name')
        doc_dept = request.POST.get('department')
        doc_phn = request.POST.get('phone')
        doc_email = request.POST.get('email')
        if request.FILES.get('image'):
            doc_image = request.FILES.get('image')
        else:
            doc_image = doctordb.objects.get(id=doc_id).doc_image
        doc_quali = request.POST.get('doc_quali')
        
        doctordb.objects.filter(id=doc_id).update(
            doc_name=doc_name,
            doc_dpt=doc_dept,
            doc_phone=doc_phn,
            doc_email=doc_email,
            doc_image=doc_image,
            doc_quali=doc_quali )
        messages.success(request, "Doctor Updated Successfully ✅")
        return redirect(doctor_list)



 #sanner pagee
def scan_page(request):
   
    return render(request, 'scan-attendance.html')

from doctorsapp.models import *
def view_attendance(request):
    attendances = Attendance.objects.all()
     # count present & absent for today
    present = attendances.filter(status='Present').count()
    total = attendances.count()
    absent = total - present
    return render(request, 'view_attend.html', {'attendances': attendances
                                                ,'present': present,
        'absent': absent})


def view_department(request):
    departments = departmentdb.objects.all()
    return render(request, 'view_dep.html', {'departments': departments})

#delete department

def delete_department(request,idd):
    department = departmentdb.objects.get(id=idd)
    department.delete()
    messages.success(request, "Department Deleted Successfully ✅")
    return redirect(view_department)

# update department
def update_department(request,idd):
    department = departmentdb.objects.get(id=idd)
    if request.method=="POST":
        dpt_name=request.POST.get("dpt_name")
        dpt_des=request.POST.get("dpt_des")
        dpt_phone=request.POST.get("dpt_phone")
        dpt_email=request.POST.get("dpt_email")
        if request.FILES.get('dpt_image'):
            dpt_image=request.FILES.get('dpt_image')
        else:
            dpt_image=departmentdb.objects.get(id=idd).dpt_image
        departmentdb.objects.filter(id=idd).update(
            dpt_name=dpt_name,
            dpt_des=dpt_des,
            dpt_phone=dpt_phone,
            dpt_email=dpt_email,
            dpt_image=dpt_image
        )
        messages.success(request, "Department Updated Successfully ✅")
        return redirect(view_department)

    
    return render(request, 'edit_department.html', {'department': department})


    #appoiment lsit
from userapp.models import *
from django.utils import timezone

def appoinment_list(request):
    appointments = appointmentdb.objects.all().order_by('-date')

    total_appointments = appointments.count()

    today = timezone.now().date()
    
    return render(request,"ad_appoinments.html",
    {
        'appointments': appointments,
        'total_appointments': total_appointments

    })

#cancel/confirm appointment status

def cancel_appointment(request, appt_id):
    appt = get_object_or_404(appointmentdb, id=appt_id)
    appt.status = 'Cancelled'
    appt.save()
    messages.success(request, "Appointment Cancelled ✅")
    return redirect(appoinment_list)

def confirm_appointment(request, appt_id):
    appt = get_object_or_404(appointmentdb, id=appt_id)
    appt.status = 'Confirmed'
    appt.save()
    messages.success(request, "Appointment Confirmed ✅")
    return redirect(appoinment_list)

def message_list(request):
    messages = ContactMessage.objects.all()
    # messages = ContactMessage.objects.all().order_by('-created_at')[:5]  
    today_messages = ContactMessage.objects.filter(created_at__date=timezone.now().date())
    appn=appointmentdb.objects.count()


    return render(request, 'messages.html', {'messages': messages
                                             ,  'today_messages': today_messages,
                                                'appn':appn})