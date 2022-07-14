# from tkinter import CASCADE
from unicodedata import name
from functools import update_wrapper
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# from base.views import room

# class Topic(models.Model):
#     name  = models.CharField(max_length=200)
    
#     def __str__(self):
#         return self.name


# # room model
# class Room(models.Model):
#     host =models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
#     topic  = models.ForeignKey(Topic, on_delete= models.SET_NULL, null=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     participants = models.ManyToManyField(User, related_name="participants", blank=True)
#     update = models.DateTimeField(auto_now = True)
#     created_date = models.DateTimeField(auto_now_add = True)
    
#     # to show the rooms created in asecending order
#     class Meta:
#         ordering = ["-update", "-created_date"]
    
#     def __str__(self):
#         return self.name
    
#     # messages to be sent
# class Messages(models.Model):
#     user = models.ForeignKey(User, on_delete= models.CASCADE)
#     room = models.ForeignKey(Room, on_delete= models.CASCADE)
#     body = models.TextField()
#     update = models.DateTimeField(auto_now=True)
#     created_date = models.DateTimeField(auto_now_add=True)
     
#     # to show the rooms created in asecending order
#     class Meta:
#         ordering = ["-update", "-created_date"]
    
    
#     def __str__(self):
#         return self.body[0:50]
    