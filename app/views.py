from random import choice
from string import ascii_uppercase, ascii_lowercase

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic, Message


def loginPage(request):
    """Login page"""
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid USERNAME or PASSWORD")

    context = {"page": page}
    return render(request, "app/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def register_user(request):
    from django.contrib.auth.forms import UserCreationForm

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "An error occurred during registration. Please try again."
            )
    return render(request, "app/login_register.html", {"form": form})


def home(request):
    """Home page"""
    q = request.GET.get("q", "")
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "app/home.html", context)


def room(request, pk):
    """Room page"""
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        if len(message.body) > 0:
            room.participants.add(request.user)
            return redirect("room", pk=room.id)
        else:
            messages.error(request, "You didn't enter any message")

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "app/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "app/profile.html", context)


def random_password(request):
    chars = ascii_uppercase + ascii_lowercase
    pwd = ""
    while len(pwd) < 8:
        pwd += choice(chars)
    context = {"password": pwd}
    messages.success(request, "Your password was successfully generated")
    return render(request, "app/password.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "app/room_form.html", context)


@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this room")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "app/room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "app/delete.html", {"obj": room})


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this room")
    if request.method == "POST":
        message.delete()
        return redirect("room", pk=message.room.id)
    return render(request, "app/delete.html", {"obj": message})
