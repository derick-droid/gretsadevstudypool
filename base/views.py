from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# creating rooms
rooms = [
    {'id':1, 'name':'let us learn python'},
    {'id':2, 'name':'Design with me'},
    {'id':3, 'name':'frontend developers'},

]

def home(request):
    return render (request, 'base/home.html',{'rooms':rooms})

def room(request):
    return render (request, 'base/room.html')