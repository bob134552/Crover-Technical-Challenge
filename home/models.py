from django.db import models

# Create your models here.
class TempData(models.Model):
    set = models.CharField(max_length=255)
    x_point = models.FloatField()
    y_point = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return self.set