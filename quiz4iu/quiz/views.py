from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from forms import CreateNewList, CreateNewQuestion, QuestionForm, RoomForm

from .models import Category, Question, Room, Topic, Message


# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            #adds user into the session
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    #page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'login_register.html',{'form':form})

def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.all().filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)        |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )
    room_count = rooms.count()
    questions = Question.objects.all().order_by('date')
    topics = Topic.objects.all()
    context = {'rooms':rooms,'questions':questions,'topics':topics,'room_count':room_count}
    return render(request,'homepage.html', context)

def say_hello(request):
    return render(request,'hello.html', { 'name':'Aleksei'})
    #return HttpResponse('Hello World')

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

def create_category(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = Category(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(request, "create_category.html", {"form":form})

def index(request,id):
    q = Question.objects.get(id=id)
    print(request)
    return render(request, 'one_question.html', {'question':q})

def index2(request,id):
    q = Question.objects.get(id=id)
    return render(request, 'one_question.html', {'question':q})



def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-date')
    particitpants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    context = {'room':room, 'room_messages':room_messages, 'particitpants':particitpants}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':room})  

@login_required(login_url='login')
def create_question(request):
    form = QuestionForm()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'question_form.html',context)

@login_required(login_url='login')
def update_question(request,pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'question_form.html',context)

@login_required(login_url='login')
def delete_question(request,pk):
    question = Question.objects.get(id=pk)
    if request.method == "POST":
        question.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':question})

@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != Message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':message})

