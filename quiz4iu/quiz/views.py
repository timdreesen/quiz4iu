from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from forms import CreateNewList, CreateNewQuestion, QuestionForm, RoomForm, LobbyForm

from .models import Category, Question, Room, Topic, Message

import itertools
import random


class Lobby:
    id_obj = itertools.count()

    def __init__(self,host,name,max_players,category):
        self.id = next(Lobby.id_obj)
        self.host = host
        self.name = name
        self.participants = [host,]
        self.max_players = max_players
        self.category = category
        self.status = 0
        questions = []

    def add_question(self,question):
        if len(self.questions) < 10:
            self.questions.append(question)

    def add_participant(self, participant):
        if len(self.participants) < self.max_players:
            self.participants.append(participant)
    
    def delete_participant(self, participant):
        try:
            self.participants.remove(participant)
        except:
            print("could not remove participant")
    
    def start_lobby(self):
        if self.status == 0:
            self.status = 1
            items = list(Question.objects.filter(category=self.category))
            self.questions = random.sample(items,5)
            print(self.status)
            for question in self.questions:
                print(question)
        else:
            pass

LobbyList = []

def fragenkatalog(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'fragenkatalog.html', {'questions':questions})


# Create your views here.
def lobby(request,pk):
    lobby = None
    for lobby2 in LobbyList:
        if lobby2.id == pk:
            lobby = lobby2
    if request.method == 'POST':
        print(request.POST)
        questions = lobby.questions
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.answer_correct)
            print()
            if q.answer_correct ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        LobbyList.remove(lobby)
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'result.html',context)
    else:
        context = {}
        if lobby.id == pk:
            context ={'lobby':lobby}
        return render(request,'lobby.html',context)


    
@login_required(login_url='login')
def create_lobby(request):
    form = LobbyForm()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = LobbyForm(request.POST)
        if form.is_valid():
            lobbyname = form.cleaned_data["name"]
            lobbymax_players = form.cleaned_data["max_players"]
            lobbycategory = form.cleaned_data["category"]
            lobby = Lobby(request.user,lobbyname,lobbymax_players,lobbycategory)
            LobbyList.append(lobby)
            return redirect('lobby',pk=lobby.id)
            #return redirect('home')
        else:
            form = LobbyForm()

    context = {'form':form}
    return render(request,'question_form.html',context)

#def lobby(request,pk):
#    context = {}
#    for lobby in LobbyList:
#        if lobby.id == pk:
#            context ={'lobby':lobby}
#    return render(request,'lobby.html',context)

def join_lobby(request,pk):
    context = {}
    for lobby in LobbyList:
        if lobby.id == pk:
            lobby.add_participant(request.user)
            context ={'lobby':lobby}
    return render(request,'lobby.html',context)

def leave_lobby(request,pk):
    context = {}
    for lobby in LobbyList:
        if lobby.id == pk:
            lobby.delete_participant(request.user)
            if len(lobby.participants)==0:
                LobbyList.remove(lobby)
                return redirect('home')
            context ={'lobby':lobby}
    return render(request,'lobby.html',context)

def start_lobby(request,pk):
    context = {}
    for lobby in LobbyList:
        if lobby.id == pk:
            lobby.start_lobby()
            context ={'lobby':lobby}
    return render(request,'lobby.html',context)

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
    categories = Category.objects.all().order_by('id')
    context = {'categories':categories,'lobbylist':LobbyList,'rooms':rooms,'questions':questions,'topics':topics,'room_count':room_count}
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

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':message})

