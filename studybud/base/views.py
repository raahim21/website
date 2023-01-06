from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from . forms import RoomModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# rooms = [
#     {'id': 1, 'name':'Lets learn Python'},
#     {'id': 2, 'name':'Lets learn JavaScript'},
#     {'id': 3, 'name':'Lets learn Css'},
# ]


def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ' error')
        
    return render(request, 'base/login-register.html', {'page': page, 'form':form})

def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('name').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not exsist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exsist')
    context = page
    return render(request, 'base/login-register.html', {'page': page})

def hi(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    )
    all_messages = Message.objects.all().order_by('-created').filter(room__topic__name__icontains=q)
    room_count = rooms.count()
    context = {'rooms': rooms}
    topics = Topic.objects.all()
    return render(request, 'base/index.html', {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'all_messages': all_messages, 'q':q})

def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    
    participants = room.participants.all()
    if request.method == "POST":
        user_msg = request.POST.get('body')
        message = Message.objects.create(body=user_msg, user=request.user, room=room)
        room.participants.add(request.user)
        message.save()
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages': comments,'participants': participants}
    return render(request, 'base/room.html', context )

def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    all_messages = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'base/profile.html', {'user':user, 'topics':topics,'all_messages':all_messages, 'rooms':rooms})

@login_required(login_url='login')
def create_room(request):
    form = RoomModel()
    if request.method == 'POST':
        form = RoomModel(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def changeRoom(request, pk):
    page = 'home'
    room = Room.objects.get(id=pk)
    form = RoomModel(instance=room)
    if request.user != room.host:
        return HttpResponse('you are not the owner of this room!')
    if request.method == 'POST':
        form = RoomModel(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form, 'page':page}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('no')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deletemessage(request, pk):
    msg = Message.objects.get(id=pk)
    room = msg.room.id
    if request.user != msg.user:
        return HttpResponse('no')
    if request.method == 'POST':
        msg.delete()
        return redirect('room', pk=room)
    return render(request, 'base/delete.html', {'obj': msg})

