# from unicodedata import name
from django.db import models

class Room(models.Model):
    # host = models.CharField(max_length=200)
    # topic  = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = models.charfield(max_lenght = 200)
    update = models.DateTimeField(auto_now = True)
    created_date = models.DateTimeField(auto_now_add = True)
    
    
    def __str__(self):
        return self.name