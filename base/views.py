from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


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

# create_rooom
def create_room(request):
    form = RoomForm
    if request.method == "POST":
        form  = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
    context = {"form" : form}
    return render(request, 'base/room_form.html', context)

# function that will update the room
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    # updating the room 
    if request.method =="POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect ("home")
    
    context = {"form":form}
    return render(request, "base/room_form.html", context)

# deleting room function

def delete_room(request, pk):
    room = Room.objects.get(id = pk)
    if request.method == "POST":
        room.delete()
        return redirect ("home")
    return render(request, "base/delete.html", {'obj': room})