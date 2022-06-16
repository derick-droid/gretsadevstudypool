# from tkinter import CASCADE
from unicodedata import name
from functools import update_wrapper
from django.db import models
from django.contrib.auth.models import User
# from base.views import room

class Topic(models.Model):
    name  = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


# room model
class Room(models.Model):
    host =models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    topic  = models.ForeignKey(Topic, on_delete= models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = models.charfield(max_lenght = 200)
    update = models.DateTimeField(auto_now = True)
    created_date = models.DateTimeField(auto_now_add = True)
    
    
    def __str__(self):
        return self.name
    
class Messages(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    