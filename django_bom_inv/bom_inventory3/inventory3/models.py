from django.db import models



class Component(models.Model):
    name = models.CharField(max_length=100, unique=True)
    available_quantity = models.IntegerField()

    def __str__(self):
        return self.name
