from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# creating rooms
# rooms = [
#     {'id':1, 'name':'let us learn python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'frontend developers'},

# ]

# home code 
def home(request):
    rooms = Room.objects.all()
    context = {"rooms":rooms}
    return render (request, 'base/home.html',context)

# room code 
def room(request, pk):
    room = Room.objects.get(id = pk)
    context = {'room':room}
    return render (request, 'base/room.html', context)

def create_room(request):
    context = {}
    return render(request, 'base/room_form.html', context)