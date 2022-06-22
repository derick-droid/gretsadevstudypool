from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



# creating rooms
# rooms = [
#     {'id':1, 'name':'let us learn python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'frontend developers'},

# ]

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, 'User doesnot exist')
            
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, "username or password does not exist")
            
    context = {}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect ("home")


# home code 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
                               
                                
    topics = Topic.objects.all()
    room_count = rooms.count() # showing number of rooms available 
    
    context = {
               "rooms":rooms,
               "topics":topics,
               "room_count":room_count
               
               }
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