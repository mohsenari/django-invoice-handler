from django.db import models

# Create your models here.

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Client(models.Model):
    INSRURANCES = (
        ('Desjardins', 'desjardins'),
        ('Sun Life', 'sunlife'),
        ('Manulife', 'manulife'),
    )
    name = models.CharField(max_length=200)
    insurance = models.CharField(max_length=20, choices=INSRURANCES)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    DOCTORS = (
        ('Bob Marley', 'bobmarly'),
        ('Emma Watson', 'emmawatson'),
        ('Snoop Dog', 'snoopdog'),
    )
    name = models.CharField(max_length=200)
    # insurance = models.CharField(max_length=20, choices=INSRURANCES)

    def __str__(self):
        return self.name
