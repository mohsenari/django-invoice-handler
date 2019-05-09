from django.db import models
from datetime import datetime

# Create your models here.

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=200)
    pub_date = models.ForeignKey('Appointment', on_delete=models.CASCADE, default=0)
    # pub_date = models.DateTimeField('date published')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, default='unnamed')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.invoice_number

class Client(models.Model):
    name = models.CharField(max_length=200)
    insurance = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    date = models.DateTimeField('available appointment date')

    def __str__(self):
        return self.date.strftime("%c")
