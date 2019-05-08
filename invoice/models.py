from django.db import models

# Create your models here.

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    client_name = models.ForeignKey('Client', on_delete=models.CASCADE, default='unnamed')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, default=0)

class Client(models.Model):
    name = models.CharField(max_length=200)
    insurance = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
