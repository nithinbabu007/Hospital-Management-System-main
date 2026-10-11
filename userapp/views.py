from django.shortcuts import render,redirect
from adminapp.models import *
from userapp.models import *
from twilio.rest import Client
import os 
from dotenv import load_dotenv
import razorpay
from django.conf import settings

from django.http import JsonResponse
import requests
load_dotenv()

# Create your views here.


# howm page user profile

def user_profile(request):
    doctors=doctordb.objects.all()
    #serach options
     # Get search values
    doctor_name = request.GET.get('doctor_name')
    specialty = request.GET.get('specialty')

    # Apply filters
    if doctor_name:
        doctors = doctordb.objects.filter(doc_name__icontains=doctor_name)

    if specialty:
        doctors = doctordb.objects.filter(doc_dpt__icontains=specialty)

    context = {
        'doctors': doctors,
        
    }
    return render(request,'home_page.html',{'doc':doctors})

# dedicated doctors listing page

def doctors_page(request):
    doctors = doctordb.objects.all()
    departments = departmentdb.objects.all()
    # search options
    doctor_name = request.GET.get('doctor_name')
    specialty = request.GET.get('specialty')

    if doctor_name:
        doctors = doctors.filter(doc_name__icontains=doctor_name)

    if specialty:
        doctors = doctors.filter(doc_dpt__icontains=specialty)

    return render(request, 'doctors_page.html', {
        'doc': doctors,
        'departments': departments,
    })

def appointment_page(request):
    departments=departmentdb.objects.all()
    
    
    return render(request,'Appointment.html',{'departments':departments})


# ajax docotr view
#AJAX Doctor View

from django.http import JsonResponse
from adminapp.models import doctordb

def get_doctors(request):

    department = request.GET.get('department')

    doctors = doctordb.objects.filter(doc_dpt=department)

    data = []

    for doctor in doctors:
        data.append({
            "id": doctor.id,
            "name": doctor.doc_name
        })

    return JsonResponse(data, safe=False)

# apooinment booking
from django.contrib import messages

def booking_appointment(request):
    if request.method == "POST":

        # Store form data in session
        request.session['appointment_data'] = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'department': request.POST.get('department'),
            'doctor': request.POST.get('doctor'),
            'date': request.POST.get('date'),
            'message': request.POST.get('message'),
        }

        # Razorpay client (demo mode: skip the real order if no keys are
        # configured, so the booking flow still works without a Razorpay
        # account; set RAZORPAY_KEY_ID/RAZORPAY_KEY_SECRET in .env to use
        # the real checkout again)
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            ))

            payment = client.order.create({
                'amount': 15000,
                'currency': 'INR',
                'payment_capture': 1
            })
            return render(request, "payment_page.html", {
                'payment': payment,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': 15000
            })

        return render(request, "payment_page.html", {
            'payment': None,
            'razorpay_key': None,
            'amount': 15000
        })

        

    #     # ✅ Call SMS function
    #     result = send_sms(obj.phone, obj.name, obj.date)

    #     # ✅ Handle responses
    #     if result == "unverified":
    #         messages.error(request, "Phone number is not verified in Twilio.")
    #     elif result == "from_error":
    #         messages.error(request, "Twilio number configuration error.")
    #     elif result == "other_error":
    #         messages.error(request, "SMS failed. Try again later.")
    #     else:
    #         obj.save()
    #         messages.success(request, "Appointment booked & SMS sent!")

    # return redirect(appointment_page)



#twilo send messages

from twilio.base.exceptions import TwilioRestException


def send_sms(phone, name, date):

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    # Demo mode: no Twilio credentials configured, so just log instead of
    # sending a real SMS (and instead of crashing the booking flow).
    if not account_sid or not auth_token:
        print(f"[demo] SMS skipped (no Twilio credentials): "
              f"Hi {name}, your appointment is booked on {date}.")
        return "skipped"

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f"Hi {name}, your appointment is booked on {date}. Your payment is successful  150 RS. See you soon!",
            from_='+17855466511',
            to=f"+91{phone}"
        )
        return "success"

    except TwilioRestException as e:
        print("Twilio Error:", e.code, e.msg)

        if e.code == 21608:
            return "unverified"

        elif e.code == 21660:
            return "from_error"

        else:
            return "other_error"
    except Exception as e:
        print("Twilio Error:", e)
        return "other_error"


#Payment Success View
def payment_success(request):
    data = request.session.get('appointment_data')

    if data:
        obj = appointmentdb.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            department=data['department'],
            doctor=data['doctor'],
            date=data['date'],
            message=data['message']
        )

    


        # Send SMS after success
        result = send_sms(obj.phone, obj.name, obj.date)
        # if result == "unverified":
        #     messages.error(request, "Phone number is not verified in Twilio.")
        # elif result == "from_error":
        #      messages.error(request, "Twilio number configuration error.")
        # elif result == "other_error":
        #      messages.error(request, "SMS failed. Try again later.")
        # else:
             
        #      messages.success(request, "Appointment booked & SMS sent!")

        messages.success(request, "Payment successful & appointment booked!")

        del request.session['appointment_data']

    return redirect(appointment_page)



#ai chat bot

def ai_chatbot(request):
    import requests

    user_message = request.GET.get('message')
    


    if not user_message:
        return JsonResponse({"reply": "No message received"})

    # Demo mode: no OpenRouter key configured, so skip the real API call
    # and give a canned hospital-assistant reply instead.
    if not settings.OPENROUTER_API_KEY:
        reply = (
            "Hi! I'm the PrimeCare assistant (demo mode, no AI key configured). "
            "I can help with appointments, doctors, and payments."
        )
        if any(word in user_message.lower() for word in ["appointment", "book", "booking"]):
            reply += '\n\n👉 Book here: <a href="/appointment_page/" target="_blank">Click to Book Appointment</a>'
        return JsonResponse({"reply": reply})

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": (
                    "You are a hospital assistant chatbot.\n"
                    "- Greet the user if they say hi/hello.\n"
                    "- Answer ONLY hospital-related queries (appointments, doctors, payments).\n"
                    "- If the question is unrelated, politely say you only handle hospital queries.\n"
                )},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)  # DEBUG

        result = response.json()

        if "choices" in result:
            bot_reply = result['choices'][0]['message']['content']
            if any(word in user_message.lower() for word in ["appointment", "book", "booking"]):
                bot_reply += '\n\n👉 Book here: <a href="/appointment_page/" target="_blank">Click to Book Appointment</a>'
        else:
            bot_reply = "API error: " + str(result)

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return JsonResponse({"reply": bot_reply})


#about page view

def about_page(request):
    return render(request, "about_page.html")

#contact page view
def service_page(request):
    return render(request, "service_page.html")


def contact_page(request):
    
    return render(request, "contact_page.html")

from django.shortcuts import render, redirect
from userapp.models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        

    return redirect(contact_page)




