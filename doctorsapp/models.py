
# Create your models here.


# models.py
from django.db import models
from adminapp.models import *
import uuid


class Attendance(models.Model):
    doctor = models.ForeignKey('adminapp.doctordb', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')],
        default='Absent'
    )
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)#uuid4 is used to generate a unique identifier for each attendance record.  
    def __str__(self):
        return f"{self.doctor} - {self.date} - {self.status}"
    
