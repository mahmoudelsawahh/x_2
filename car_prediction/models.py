from django.db import models

class Car(models.Model):

    MODEL_CHOICES = (('A1','A1'),('A2', 'A2'),('A3', 'A3'),('A4', 'A4'),('A5', 'A5'),
    ('A6', 'A6'),('A7', 'A7'),('A8', 'A8'),('Q2', 'Q2'),('Q5', 'Q5'),('Q7', 'Q7'),('Q8', 'Q8'),
    ('R8', 'R8'),('RS3', 'RS3'),('RS4', 'RS4'),('RS5', 'RS5'),('RS6', 'RS6'),('RS7', 'RS7'),
    ('S3', 'S3'),('S4', 'S4'),('S5', 'S5'),('S8', 'S8'),('SQ5', 'SQ5'),('SQ7', 'SQ7'),('TT', 'TT'))
    model = models.CharField(max_length=150, choices=MODEL_CHOICES)
    ## Year from 1998-2019
    year = models.IntegerField(null=True) 
    price = models.IntegerField(null=True)
    TRANS_CHOICES = (('Manual','Manual'),('Semi-Auto', 'Semi-Auto'),('Automatic', 'Automatic'))
    transmission = models.CharField(max_length=10, choices=TRANS_CHOICES)
    mileage = models.IntegerField(null=True)
    FUEL_CHOICES = (('Diesel','Diesel'),('Petrol', 'Petrol'),('Hybrid', 'Hybrid'))
    fuel_type = models.CharField(max_length=6, choices=FUEL_CHOICES)
    tax = models.IntegerField(null=True)
    mpg = models.FloatField(null=True)
    ## Engine Size from 1.0 - 6.3
    engine_size = models.FloatField(null=True)
    
    def __str__(self):
        return self.model