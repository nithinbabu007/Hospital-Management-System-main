from django.db import models



# Create your models here.
# department db
class departmentdb(models.Model):
    dpt_name = models.CharField(max_length=100, unique=True)
    dpt_des = models.TextField(max_length=1000)
    dpt_phone=models.TextField(max_length=10)
    dpt_email=models.EmailField(max_length=100)

    dpt_image = models.ImageField(upload_to='departments/', blank=True, null=True)

    def __str__(self):
        return self.dpt_name

# employee db
class doctordb(models.Model):
    doc_name = models.CharField(max_length=100)
    doc_dpt = models.TextField(max_length=1000)
    doc_phone=models.TextField(max_length=10,unique=True)
    doc_email=models.EmailField(max_length=100)
    doc_quali=models.TextField(max_length=100,default="MBBS")

    doc_image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return self.doc_name

