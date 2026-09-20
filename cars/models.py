from django.db import models

# Create your models here.

class Car(models.Model):
    mpg = models.FloatField()
    cylinders = models.IntegerField()
    displacement = models.FloatField()
    horsepower = models.FloatField(null=True, blank=True)
    weight = models.IntegerField()
    acceleration = models.FloatField()
    model_year = models.IntegerField()
    origin = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
