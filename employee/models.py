from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils import timezone
# Create your models here.
def default_expiry_date():
    return timezone.now().date() + timedelta(days=365)
class EmployeeDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    empcode = models.CharField(max_length=100, null=True)
    empdept = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=20, null=True)
    joiningdate = models.DateField(default=date.today)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)  # Add this line

    coverage = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True, blank=True)  # Date of Birth

    tehsil = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    blood_group = models.CharField(max_length=3, null=True)# Assuming blood group as a short string like "A+", "B-", etc.
    expiry_date = models.DateField(default=default_expiry_date)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DOC_PENDING', 'Document Pending'),
        ('DOC_VERIFIED', 'Document Verified'),
        ('CONTRACT_PENDING', 'Contract Pending'),
        ('FINALIZED', 'Finalized'),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='PENDING')
    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = self.joiningdate + timedelta(days=365)
        super(EmployeeDetail, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username
    def custom_employee_code(self):
        district_code = self.district[:4].upper()+"/" if self.district != "All Gujarat" else ""
        return f"GJ/{district_code}{self.empcode}" 

class EmployeeEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    coursepg = models.CharField(max_length=100, null=True)
    schoolclgpg = models.CharField(max_length=200,null=True)
    yearpassingpg = models.CharField(max_length=20,null=True)
    percentagepg = models.CharField(max_length=30, null=True)
    coursegra = models.CharField(max_length=100, null=True)
    schoolclggra = models.CharField(max_length=200, null=True)
    yearpassinggra = models.CharField(max_length=20, null=True)
    percentagegra = models.CharField(max_length=30, null=True)
    coursessc = models.CharField(max_length=100, null=True)
    schoolclgssc = models.CharField(max_length=200, null=True)
    yearpassingssc = models.CharField(max_length=20, null=True)
    percentagessc = models.CharField(max_length=30, null=True)
    coursehsc = models.CharField(max_length=100, null=True)
    schoolclghsc = models.CharField(max_length=200, null=True)
    yearpassinghsc = models.CharField(max_length=20, null=True)
    percentagehsc = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.user.username


class EmployeeExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company1name = models.CharField(max_length=100, null=True)
    company1desig = models.CharField(max_length=100, null=True)
    company1salary = models.CharField(max_length=100, null=True)
    company1duration = models.CharField(max_length=100, null=True)
    company2name = models.CharField(max_length=100, null=True)
    company2desig = models.CharField(max_length=100, null=True)
    company2salary = models.CharField(max_length=100, null=True)
    company2duration = models.CharField(max_length=100, null=True)
    company3name = models.CharField(max_length=100, null=True)
    company3desig = models.CharField(max_length=100, null=True)
    company3salary = models.CharField(max_length=100, null=True)
    company3duration = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
    
class Document(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhaar_card = models.FileField(upload_to='documents/', null=True, blank=True)
    pan_card = models.FileField(upload_to='documents/', null=True, blank=True)
    light_bill = models.FileField(upload_to='documents/', null=True, blank=True)
    photo = models.FileField(upload_to='documents/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.username} - Documents"


class SignedContract(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.FileField(upload_to='contracts/')
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)  # Add this line
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee.username} - Contract'
