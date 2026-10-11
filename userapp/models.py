from django.db import models

# Create your models here.
class appointmentdb(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    department = models.TextField(max_length=100)
    doctor = models.TextField(max_length=100)

    date = models.DateField()
    message = models.TextField(blank=True)

    # Appointments are only ever created after a successful payment (see
    # payment_success in userapp/views.py), so a newly booked appointment
    # is "Confirmed" by default.
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Confirmed',
    )

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name