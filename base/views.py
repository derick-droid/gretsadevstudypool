from email import message
from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Messages, User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# creating rooms
# rooms = [
#     {'id':1, 'name':'let us learn python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'frontend developers'},

# ]

def login_page(request):
    page = "login" # register
    
    # preventing relogin 
    if request.user.is_authenticated:
        return redirect ("home")
    
    
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            
        except:
            messages.error(request, 'User doesnot exist')
            
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, "username or password does not exist")
            
    context = {
        "page": page,
    }
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect ("home")

def register_user(request):
    form = MyUserCreationForm()
    
    if request.method == "POST":
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower() # making the name in lower case
                user.save()
                login(request, user)
                return redirect ("home")
            else:
                messages.error(request, "An error occured during registration process")

        
    
    
    return render(request, 'base/login_register.html', {"form" : form})


# home code 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
                               
                                
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count() # showing number of rooms available 
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains = q))
    
    context = {
               "rooms":rooms,
               "topics":topics,
               "room_count":room_count,
               "room_messages":room_messages,
               
               }
    return render (request, 'base/home.html',context)

# room code 
def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.messages_set.all().order_by("-created_date")
    participants = room.participants.all() 
    
    if request.method == "POST":  
               
     message = Messages.objects.create(
         user = request.user,
         room = room,
         body = request.POST.get("body"),
         
     )
     room.participants.add(request.user)
     return redirect ("room", pk = room.id)
   
    
    context = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants
               }
    return render (request, 'base/room.html', context)


# creating user profile 
def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.messages_set.all()
    topics  =Topic.objects.all()
    context = { "user": user,
               "rooms": rooms, 
               "room_messages":room_messages,
               "topics":topics,
                 
     }
    
    return render(request, "base/profile.html", context)



@login_required(login_url = "/login")
# create_rooom
def create_room(request):
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic") 
        topics, create = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create (
            host = request.user,
            topic = topics,
            name = request.POST.get("name"),  
            description = request.POST.get("description")  
        )
       
        return redirect("home")
        
    context = {
        "form" : form,
        "topics" : topics
        }
    return render(request, 'base/room_form.html', context)


@login_required(login_url = "/login")
# function that will update the room
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host: # blocking unauthorized
        return HttpResponse("You are not the authorized to update")
    
    # updating the room 
    if request.method =="POST":
        topic_name = request.POST.get("topic") 
        topics, create = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get("name")
        room.topic = topics
        room.description = request.POST.get("description")
        room.save()

        return redirect ("home") 
       
    
    context = {
        "form":form,
        "topics":topics,
        "room":room,
        }
    return render(request, "base/room_form.html", context)


# deleting room function
@login_required(login_url = "/login")
def delete_room(request, pk):
    room = Room.objects.get(id = pk)
    
    if request.user != room.host: # blocking unauthorized
      return HttpResponse("You are not the authorized to delete this room ")
    
    
    if request.method == "POST":
        room.delete()
        return redirect ("home")
    return render(request, "base/delete.html", {'obj': room})

# deleting a message
@login_required(login_url = "/login") # the user is logged in before deleting
def delete_message(request, pk):
    message= Messages.objects.get(id = pk)
    
    if request.user != message.user: # blocking unauthorized
      return HttpResponse("You are not the authorized to delete this message ")
    
    
    if request.method == "POST":
        message.delete()
        return redirect ("home")
    return render(request, "base/delete.html", {'obj': message})

# user updating own profile
@login_required(login_url = "login")
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect("user-profile", pk = user.id )
    
    context = {
        "form":form
    }
    return render(request,"base/update-user.html", context)

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains = q)
    context = {
        "topics": topics
    }
    return render(request, 'base/topics.html', context)


# activities update
def activities(request):
    room_messages = Messages.objects.all()
    context = {'room_messages':room_messages
        
    }
    return render(request, "base/activity.html", context)
    
    